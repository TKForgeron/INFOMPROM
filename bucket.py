# from logging import raiseExceptions
# from nptyping import NDArray, Bool, Shape
import warnings
import pandas as pd
from typing import Any
from custom_models import Average, Minimum, Maximum, Sample_mean, Median, Mode
from sklearn.linear_model import LassoLarsCV, LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor


class Bucket:
    def __init__(
        self,
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
            model_type : [str]
                Machine learning model by which predictions will be made.
            seed : [int]
                Controls the randomness that some models can have.
            cv : [int]
                Determines the number of folds used in the cross-validation process.

        """

        self.data = data
        self.model_up_to_date = True
        self.model = self.configure_model(model_type, cv, seed)

    def configure_model(model_type, cv, seed):

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
            warnings.warn("Model type unknown, we resort to using linear regression")
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

    def append(self, row: dict) -> None:

        if type(row) == dict:
            self.data.append(row)
        else:
            raise Exception(
                "You are trying to append something else than a dict to a list of dict"
            )

    def finalize(self) -> None:
        self.transform_data()
        print("Data transformed to pd.DataFrame")
        X = self.data.iloc[:, :-2]  # everything until remaining time
        y = self.data.iloc[:, -2]  # remaining time
        self.model.fit(X, y)
        print(f"{self.model_type} model fitted to bucketed training data")
