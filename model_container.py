import pandas as pd
from nptyping import NDArray, Bool, Shape
from typing import Any
import river


class Bucket:
    def __init__(
        self, data: pd.DataFrame, model_type: str = "avg", seed: int = 42
    ) -> None:
        self.data = data
        self.model_up_to_date = True
        self.model = self.init_model(model_type, seed)

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
            model = river.ensemble.AdaptiveRandomForestRegressor(seed=seed)

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