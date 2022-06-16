# from logging import raiseExceptions
# from nptyping import NDArray, Bool, Shape
import warnings
import pandas as pd
from src.preprocessor import Preprocessor
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from sklearn.linear_model import (
    LassoLarsCV,
    LinearRegression,
    LogisticRegression,
    ElasticNetCV,
)
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor


class Bucket:
    # TODO fix sklearn models
    # TODO make OHE cols of all activities found
    # TODO predict moet per unfinished trace een prediction geven
    # TODO check if append() works
    # TODO integrate a scoring function (e.g. MAE, MSE, Cross Entropy)
    # TODO train val split

    def __init__(
        self,
        y_col: str,
        data: pd.DataFrame = None,
        encoding_operation: str = None,
        model_type: str = "avg",
        seed: int = 42,
        cv: int = 5,
    ) -> None:
        """
        Initializes a Bucket.

        Parameters
        ----------
            data : [pd.DataFrame]
                A subset of a complete event log, filtered by states using
                an Annotated Transition System.
                At initialization (in an ATS node) this is a list of dictionaries.
                When the ATS is fully constructed, this attribute will be transformed
                to a pandas dataframe.
            y : [str]
                Column name of the target variable.
            seed : [int]
                Controls the randomness that some models can have.
            cv : [int]
                Determines the number of folds used in the cross-validation process.

        """

        # for making predictions, model input should have cols equal to train data
        self.x_cols = []

        self.data = data
        self.preprocessor = Preprocessor(y_col, encoding_operation)
        self.model = self.configure_model(model_type, cv, seed)
        # self.model_up_to_date = True

    def configure_model(self, model_type: str, cv: int, seed: int):

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
            warnings.warn("Model type unknown, resorting to using linear regression")
            model = LinearRegression()

        return model

    def append(self, row: dict) -> None:

        if type(row) == dict:
            self.data.append(row)
        else:
            raise Exception(
                "You are trying to append something else than a dict to a list of dict"
            )

    def predict_one(self, pred_x) -> None:

        return self.model.predict(pred_x)[0]

    def finalize(self) -> None:

        print("Transforming data to pd.DataFrame...")
        self.data = self.preprocessor.transform_data(self.data)

        print("Encoding data...")
        self.data, self.x_cols = self.preprocessor.encode(self.data)
        print(self.x_cols)
        print(len(self.x_cols))

        print("Generating train-test-split...")
        X, y = self.preprocessor.generate_split(self.data, test_size=0.8)

        print(f"Fitting {self.model} model to training data of bucket...")
        self.model.fit(X, y)
