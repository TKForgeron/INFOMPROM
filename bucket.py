import pandas as pd
from nptyping import NDArray, Bool, Shape
from typing import Any
from sklearn.linear_model import LassoLarsCV


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
        self.model = self.init_model(model_type, seed)
        self.seed = seed
        self.cv = cv

    def finalize() -> None:
        # transform_data
        # model.fit
        pass

    def transform_data() -> None:
        # transform self.data from list of dict to df
        pass

    def append_row(self, row: NDArray[Any, Any]) -> None:
        self.data = np.append(self.data, [row], axis=0)

    def init_model(self, model_type, seed):
        if model_type == "avg":
            model = self.avg_predictor()
        elif model_type == "RF" or model_type == "rf":
            model = LassoLarsCV(seed=seed)

        return model

    def avg_predictor():
        pass


# class Data:

#     def _init_(self, prediction_type) -> None:

#         self.numpy_array = []
#         predict_col = 'x'
#         agg_function = init_predictor()


#     def init_predictor(prediction_type):

#         if prediction_type = RF:

#             return model

#     def add_to_data():

#         update_model


#     def predict(self, row):

#         self.agg_function.predict

#     def calc_avg():


# dict = {x: 1, y: 2 , z:3}

# cols = dict.keys # = [x,y,z]

# 'x' = 0
