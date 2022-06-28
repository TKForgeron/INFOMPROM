import numpy as np
from sklearn.metrics import r2_score  # , mean_squared_error


def get_mae_rmse(y_test, y_preds) -> tuple[float, float, float]:

    r2 = r2_score(y_test, y_preds)

    if type(y_test) != np.array:
        y_test = np.array(y_test)

    if type(y_preds) != np.array:
        y_preds = np.array(y_preds)

    mse = (np.square(y_test - y_preds)).mean(axis=None)
    rmse = mse**0.5
    mae = (np.abs(y_test - y_preds)).mean(axis=None)

    return mae, rmse, r2


def get_ae_vector(y_test, y_preds) -> list[float]:

    if type(y_test) != np.array:
        y_test = np.array(y_test)

    if type(y_preds) != np.array:
        y_preds = np.array(y_preds)

    ae = np.abs(y_test - y_preds).tolist()

    return ae
