import numpy as np


def get_mae_mse(y_test, y_preds) -> float:
    # mae = 0.0
    # mse = 0.0
    if type(y_test) != np.array:
        y_test = np.array(y_test)

    if type(y_preds) != np.array:
        y_preds = np.array(y_preds)

    mse = (np.square(y_test - y_preds)).mean(axis=None)
    mae = (np.abs(y_test - y_preds)).mean(axis=None)
    # for y_pred, y in y_preds, y_test:
    #     mae += abs(y_pred - y)
    #     mse += (y_pred - y) ** 2

    # n = len(y_test)
    # mae = mae / n
    # mse = mse / n

    return mae, mse
