import numpy as np
from nptyping import NDArray, Bool, Shape
from typing import Any


class Model_container:
    def __init__(self, data: NDArray[Any, Any]) -> None:
        self.data = data
        self.model_up_to_date = True

    def append_row(self, row: NDArray[Any, Any]) -> None:
        self.data = np.append(self.data, [row], axis=0)


# class Data:

#     def _init_(self, prediction_type) -> None:

#         self.numpy_array = []
#         predict_col = 'x'
#         agg_function = init_predictor()


#     def init_predictior(prediction_type):

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
