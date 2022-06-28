import pickle
from src.globals import *
from src.metrics import get_mae_rmse
import numpy as np

y_cols = (TIME_TARGET_COLUMN, ACTIVITY_TARGET_COLUMN)

for target_var, y_col in zip(TARGET_VARS, y_cols):

    # get same preprocessed input data as used in our actual experiment
    with open(f"data/{INPUTDATA_OBJECT}_{target_var}.pkl", "rb") as file:
        input = pickle.load(file)

    # use same split as for the advanced models
    _, _, y_train, y_test = input.train_test_split_on_trace(
        y_col=y_col, ratio=0.8, seed=RANDOM_SEED
    )

    y_test = np.array(y_test)
    y_preds_mean = np.array([y_train.mean()] * len(y_test))
    y_preds_median = np.array([y_train.median()] * len(y_test))
    y_train_mode = y_train.mode().tolist()
    y_preds_mode = np.array([y_train_mode[len(y_train_mode) // 2]] * len(y_test))

    mae_mean, rmse_mean, r2_mean = get_mae_rmse(y_test, y_preds_mean)
    mae_median, rmse_median, r2_median = get_mae_rmse(y_test, y_preds_median)
    mae_mode, rmse_mode, r2_mode = get_mae_rmse(y_test, y_preds_mode)

    print("-" * 64)
    print()

    if y_col == y_cols[0]:
        print(f"Naive Mean predicting {y_col}")
        print(f"R^2: {r2_mean}")
        # get difference in hours instead of seconds
        print(
            f"MAE: {round(mae_mean/ (60*60))} hours  = {round(mae_mean / (60*60*24))} days"
        )
        print(
            f"RMSE: {round(rmse_mean/ (60*60))} hours  = {round(rmse_mean / (60*60*24))} days"
        )
        print()

        print(f"Naive Median predicting {y_col}")
        print(f"R^2: {round(r2_median,3)}")
        # get difference in hours instead of seconds
        print(
            f"MAE: {round(mae_median/ (60*60))} hours  = {round(mae_median / (60*60*24))} days"
        )
        print(
            f"RMSE: {round(rmse_median/ (60*60))} hours  = {round(rmse_median / (60*60*24))} days"
        )
        print()

        print(f"Naive Mode predicting {y_col}")
        print(f"R^2: {round(r2_mode,3)}")
        # get difference in hours instead of seconds
        print(
            f"MAE: {round(mae_mode/ (60*60))} hours  = {round(mae_mode / (60*60*24))} days"
        )
        print(
            f"RMSE: {round(rmse_mode/ (60*60))} hours  = {round(rmse_mode / (60*60*24))} days"
        )
        print()
    else:
        print(f"Naive Mean predicting {y_col}")
        print(f"R^2: {r2_mean}")
        print(f"MAE: {round(mae_mean,2)} activities")
        print(f"RMSE: {round(rmse_mean,2)} activities")
        print()

        print(f"Naive Median predicting {y_col}")
        print(f"R^2: {round(r2_median,3)}")
        print(f"MAE: {round(mae_median,2)} activities")
        print(f"RMSE: {round(rmse_median,2)} activities")
        print()

        print(f"Naive Mode predicting {y_col}")
        print(f"R^2: {round(r2_mode,3)}")
        print(f"MAE: {round(mae_mode,2)} activities")
        print(f"RMSE: {round(rmse_mode,2)} activities")
        print()
