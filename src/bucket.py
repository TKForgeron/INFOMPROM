# from logging import raiseExceptions
# from nptyping import NDArray, Bool, Shape
from msilib import type_key
import warnings
import pandas as pd
from src.bucket_preprocessor import Preprocessor
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from sklearn.linear_model import (
    LassoLarsCV,
    LinearRegression,
    LogisticRegression,
    ElasticNetCV,
)
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import cross_val_score


class Bucket:
    # TODO fix sklearn models
    # TODO make OHE cols of all activities found
    # TODO predict moet per event een prediction geven
    # ✓ TODO check if append() works
    # TODO integrate a scoring function (e.g. MAE, MSE, Cross Entropy)
    # TODO train val split
    # TODO implement cross_val_score()

    def __init__(
        self,
        id: int,
        x_cols: list[str],
        y_col: str,
        data: list[dict],
        encoding_operation: str = None,
        model_type: str = None,
        seed: int = None,
        cv: int = None,
    ) -> None:
        """
        Initializes a Bucket.

        Parameters
        ----------
            data : [list[dict]]
                A subset of a complete event log, filtered by states using
                an Annotated Transition System.
                At initialization (in an ATS node) this is a list of dictionaries.
            y_col : [str]
                Column name of the target variable.
            x_cols : [list[str]]
                Column names of the feature variables. Initially these are set by the
                State. Upon encoding the data these are updated, as some columns may
                be dropped or added.
            seed : [int]
                Controls the randomness that some models can have.
            cv : [int]
                Determines the number of folds used in the cross-validation process.

        """

        # for making predictions, model input should have cols equal to train data
        self.id = id
        self.x_cols = x_cols
        self.y_col = y_col
        self.X = None  # pd.DataFrame
        self.y = None  # pd.Series
        self.data = data
        # preprocessor will probably be removed
        self.preprocessor = Preprocessor(y_col, encoding_operation)
        if seed is None:
            seed = 42
        if cv is None:
            cv = 5
        self.cv = cv
        self.model = self.configure_model(model_type, cv, seed)
        self.mean_accuracy = None  # float
        # self.model_up_to_date = True

    def append(self, row: dict) -> None:
        # Could add check if added event has same keys as self.x_cols,
        # as this should be the case
        # self.x_cols == list(row.keys())

        if type(row) == dict:
            self.data.append(row)
        else:
            raise Exception(
                "You are trying to append something else than a dict to a list of dict"
            )

    def _transform_data(self) -> None:

        # Bucket0 belongs to the empty state, which has no data?
        self.X = pd.DataFrame(self.data)
        self.y = pd.Series(self.X[self.y_col])
        self.X = self.X[self.x_cols]

    def configure_model(self, model_type: str, cv: int, seed: int):

        if model_type is not None:

            if model_type.upper() == "SAMPLEMEAN":
                model = SampleMean()
            elif model_type.upper() == "AVG":
                model = Average()
            elif model_type.upper() == "MIN":
                model = Minimum()
            elif model_type.upper() == "MAX":
                model = Maximum()
            elif model_type.upper() == "MEDIAN":
                model = Median()
            elif model_type.upper() == "MODE":
                model = Mode()
            elif model_type.upper() == "LINREG":
                model = LinearRegression()
            elif model_type.upper() == "LOGREG":
                model = LogisticRegression()
            elif model_type.upper() == "HGB":
                model = HistGradientBoostingRegressor()
            elif model_type.upper() in [
                "ELASTICNET",
                "ELASTICNETCV",
            ]:
                model = ElasticNetCV(cv=cv)
            elif model_type.upper() in ["LASSOLARSCV", "LASSOLARS"]:
                model = LassoLarsCV(cv=cv)
            elif model_type.upper() == "RF":
                model = RandomForestRegressor(n_estimators=10, random_state=seed)
            else:
                warnings.warn(
                    "Model type unknown, resorting to using linear regression"
                )
                model = LinearRegression()
        else:
            warnings.warn("Model type unknown, resorting to using linear regression")
            model = LinearRegression()

        return model

    def cross_validate(self) -> None:
        try:
            if self.model.is_custom_model:
                self.score_custom_model()
        except:
            scores = cross_val_score(
                self.model,
                self.data[self.x_cols],
                self.data[self.preprocessor.y_col],
                cv=self.cv,
                n_jobs=-1,
            )

            self.mean_accuracy = scores.mean()

    def score_custom_model(self) -> None:
        try:
            if self.model.is_custom_model:
                print(f"Scoring {self.model} model...")

        except:
            warnings.warn("score_custom_model() applied to a non-custom model.")

    def predict_one(self, pred_x) -> None:

        return self.model.predict(pred_x)[0]

    def finalize(self) -> None:
        print(f"Finalizing Bucket {self.id}...")
        if self.id != 0:
            # print("Transforming data to pd.DataFrame...")
            self._transform_data()

            # print("Encoding data...")
            # self.data, self.x_cols = self.preprocessor.encode(self.data)
            # print(self.x_cols)
            # print(len(self.x_cols))

            # # mss is het doordat x_cols van boven gedefinieerd wordt

            # print("Generating train-test-split...")
            # X, y = self.preprocessor.generate_split(self.data, test_size=0.8)

            print(f"Fitting {self.model} model to training data of Bucket {self.id}...")
            self.model.fit(self.X, self.y)
