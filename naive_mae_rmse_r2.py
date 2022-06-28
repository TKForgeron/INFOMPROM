import pickle
from src.globals import *
from src.metrics import get_ae_vector, get_mae_rmse
import numpy as np
import pandas as pd

y_cols = [TIME_TARGET_COLUMN, ACTIVITY_TARGET_COLUMN]

for target_var, y_col in zip(TARGET_VARS, y_cols):

    # get same preprocessed input data as used in our actual experiment
    with open(f"data/{INPUTDATA_OBJECT}_{target_var}.pkl", "rb") as file:
        input = pickle.load(file)

    # use same split as for the advanced models
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
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

    ae_mean = get_ae_vector(y_test, y_preds_mean)
    ae_median = get_ae_vector(y_test, y_preds_median)
    ae_mode = get_ae_vector(y_test, y_preds_mode)

    for model, ae in zip(
        ["NaiveMean()", "NaiveMedian()", "NaiveMode()"], [ae_mean, ae_median, ae_mode]
    ):
        if y_col == TIME_TARGET_COLUMN:
            ae_in_hours = list(map(lambda x: x / 60 / 60, ae))
            ae = ae_in_hours
            from statistics import mean

        print(mean(ae))
        with open(f"data/ae_{target_var}_{model}.pkl", "wb") as file:
            pickle.dump(ae, file)

    print("-" * 64)
    print()

    if y_col == TIME_TARGET_COLUMN:
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

    # don't use split, VERY NAIVE METHOD, only for Data Description section in paper
    X = pd.concat([X_train, X_test], axis=0)
    y = np.concatenate((y_train, y_test), axis=0)

    very_naive_y_preds_mean = np.array([y.mean()] * len(y))
    very_naive_ae_mean = get_ae_vector(y, very_naive_y_preds_mean)
    very_naive_ae_mean_in_days = list(
        map(lambda x: x / 60 / 60 / 24, very_naive_ae_mean)
    )
    with open(f"data/ae_{target_var}_VeryNaiveMean().pkl", "wb") as file:
        pickle.dump(very_naive_ae_mean_in_days, file)
