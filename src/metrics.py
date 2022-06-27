import numpy as np


def get_mae_mse(y_test, y_preds) -> float:

    if type(y_test) != np.array:
        y_test = np.array(y_test)

    if type(y_preds) != np.array:
        y_preds = np.array(y_preds)

    mse = (np.square(y_test - y_preds)).mean(axis=None)
    mae = (np.abs(y_test - y_preds)).mean(axis=None)

    return mae, mse
