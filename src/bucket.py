# from logging import raiseExceptions
# from nptyping import NDArray, Bool, Shape
import warnings
import pandas as pd
from src.custom_models import Average, Minimum, Maximum, Sample_mean, Median, Mode
from sklearn.linear_model import LassoLarsCV, LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor


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

        self.data = data
        self.y = y_col
        self.model = self.configure_model(model_type, cv, seed)
        # self.model_up_to_date = True

    def configure_model(self, model_type: str, cv: int, seed: int):

        if model_type.upper() == "SAMPLEMEAN":
            model = Sample_mean()
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

    def transform_data(self) -> None:
        # transform self.data from list of dict to df

        if type(self.data) == pd.DataFrame:
            warnings.warn(
                "You are trying to transform Bucket data to pd.DataFrame, but it is already a pd.DataFrame"
            )

        else:
            self.data = pd.DataFrame(self.data)
            self.data = self.data.iloc[:, :-1]

    def append(self, row: dict) -> None:

        if type(row) == dict:
            self.data.append(row)
        else:
            raise Exception(
                "You are trying to append something else than a dict to a list of dict"
            )

    def encode(self, operation_type: str = None) -> None:
        if operation_type == "ohe":
            pass
        else:
            # remove all non-numerical cols
            self.data = self.data.select_dtypes(["number"])
        # cumulated sum OHE
        pass

    def _generate_split(self) -> None:
        y_col_index_no = self.data.columns.get_loc(self.y)
        X = self.data.iloc[:, :y_col_index_no]  # everything up to y_column
        y = self.data.loc[self.y]  # y_column
        print(X)
        # NOT DONE YET, ADD ACTUAL TRAIN TEST SPLIT

        return X, y

    def predict(self, pred_x) -> None:
        return self.model.predict(pred_x)[0]

    def finalize(self) -> None:
        print("Transforming data to pd.DataFrame...")
        self.transform_data()
        print("Encoding data...")
        self.encode("num_cols_only")
        print("Generating train-test-split...")
        X, y = self._generate_split()
        print(f"Fitting {self.model} model to bucketed training data...")
        self.model.fit(X, y)
