from logging import raiseExceptions
from debugpy import configure
import pandas as pd

# from nptyping import NDArray, Bool, Shape
from typing import Any
from custom_models import Average, Minimum, Maximum, Sample_mean
from sklearn.linear_model import LassoLarsCV, LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor


class Bucket:
    def __init__(
        self, data: pd.DataFrame, model_type: str = "avg", seed: int = 42, cv: int = 5
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
                Controls both the randomness that some models could have.
            cv : [int]
                Determines the number of folds used in the cross-validation process.

        """

        self.data = data
        self.model_up_to_date = True
        self.seed = seed
        self.cv = cv
        self.model_type = model_type
        self.model = self.configure_model()

    def configure_model(self):

        if self.model_type.upper() in ["AVG", "AVERAGE", "MEAN"]:
            model = Average()
        elif self.model_type.upper() in ["MIN", "MINIMUM"]:
            model = Minimum()
        elif self.model_type.upper() in [
            "MAX",
            "MAXIMUM",
        ]:
            model = Maximum()
        elif self.model_type.upper() in [
            "SAMPLE MEAN",
            "SAMPLE_MEAN",
            "SAMPLEMEAN",
        ]:
            model = Sample_mean()
        elif self.model_type.upper() in [
            "LIN",
            "LINEAR REGRESSION",
            "LINREG",
        ]:
            model = LinearRegression()
        elif self.model_type.upper() in [
            "ELASTICNET",
            "ELASTICNETCV",
        ]:
            model = ElasticNetCV(cv=self.cv)
        elif self.model_type.upper() in ["LASSOLARSCV", "LASSOLARS"]:
            model = LassoLarsCV(cv=self.cv)
        elif self.model_type.upper() in [
            "RF",
            "RANDOMFOREST",
            "RANDOM FOREST",
            "RANDOM_FOREST",
        ]:
            model = RandomForestRegressor(n_estimators=10, random_state=self.seed)

        return model

    def transform_data(self) -> None:
        # transform self.data from list of dict to df

        if type(self.data) == pd.DataFrame:
            raise Warning(
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

        self.model.fit()
        print(f"{self.model_type} model fitted to bucketed training data")
