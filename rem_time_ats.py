# External imports
import pickle
from time import time
import pandas as pd
from sklearn.linear_model import (
    LinearRegression,  # linear, no outliers in data, no correlation between features
    TheilSenRegressor,  # linear, no outliers in data, correlation between features
    Lars,  # linear, outliers in data, speed important, more features than samples, MAE: 325
    ARDRegression,  # linear, outliers in data, speed important, few important features,
    SGDRegressor,  # linear, outliers in data, speed important, large dataset
    BayesianRidge,  # linear, outliers in data, speed important, not especially large dataset
)
from sklearn.neighbors import (
    KNeighborsRegressor,  # MAE: 46
    RadiusNeighborsRegressor,
)  # nonlinear, many features, few important features, sample/feature ratio: high sample
from sklearn.svm import (
    SVR,  # nonlinear, many features, outliers in data, few important features, sample/feature ratio: high feature (TAKES VEEERY LONG)
)
from sklearn.ensemble import (
    HistGradientBoostingRegressor,  # nonlinear, <10 features, no noise/outliers, >10000 samples, robust against missing values
    RandomForestRegressor,
    BaggingRegressor,
    AdaBoostRegressor,
)

# Internal imports
from src.ats import *
from src.print_ats import *
from src.input_data import InputData
from src.custom_models import Mean, Median, Mode, Minimum, Maximum, SampleMean
from src.metrics import get_mae_rmse
from src.helper import print_progress_bar
from src.globals import (
    PREPROCESSING_IN_FILE,
    INPUTDATA_OBJECT,
    BASE_ATS_OUT_FILE,
    RANDOM_SEED,
    TIME_TARGET_COLUMN,
)


if __name__ == "__main__":

    target_var = "rem_time"
    y_col = TIME_TARGET_COLUMN

    try:
        raise Exception("tuning data prepprocessing step")
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}_{target_var}.pkl")
    except:
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_standard_preprocessing(
            agg_col=target_var,  # calculated y column
            filter_incompletes=True,
            date_cols="auto",
        )

        # columns that have <20 unique values are one-hot encoded
        input.use_cat_encoding_on(
            "ohe", ["Asset Type Affected", "Status", "Closure Code"]
        )

        # columns that have ordinal values are label encoded
        input.use_cat_encoding_on("label", ["Category", "Priority"])

        # columns with too many categories are deleted
        input.use_cat_encoding_on(
            "none",
            [
                "Service Affected",
                "Asset Affected",
                "Asset SubType Affected",
                "Service Caused",
                "Assignment Group",
                "Asset Caused",
                "Asset Type Caused",
                "Asset SubType Caused",
            ],
        )

        # drop missing values, as most models don't accept this
        # we drop per column, as then only 4 will be lost
        input.dropna(axis=1)

        input.save_df(
            n_rows=20
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(f"{INPUTDATA_OBJECT}_{target_var}")

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=y_col, ratio=0.8, seed=RANDOM_SEED
    )

    # pickling y_test
    with open(f"data/y_test_{target_var}.pkl", "wb") as file:
        pickle.dump(y_test, file)

    X_test = input.add_prev_events(X_test)

    # If ATS already fitted (not finalized)
    # with open(f"data/{BASE_ATS_OUT_FILE}_{target_var}.pkl", "rb") as file:
    #     ats = pickle.load(file)

    ats = ATS(
        trace_id_col="Incident ID",
        act_col="Activity",
        y_col=y_col,
        representation="multiset",
        horizon=1,
        seed=RANDOM_SEED,
    )
    ats.fit(X_train, y_train)
    ats.save(f"{BASE_ATS_OUT_FILE}_{target_var}")

    ats.finalize(model=Mean())

    print_progress_bar(
        0, len(y_test), prefix="Prediction:", suffix="Complete", length=50
    )

    y_preds = []

    for i, event in enumerate(X_test.to_dict(orient="records")):

        y_preds.append(ats.predict(event))
        print_progress_bar(
            i + 1, len(y_test), prefix="Prediction:", suffix="Complete", length=50
        )

    # pickling all predicted values into a pickled variable with name of the model used
    with open(f"data/y_preds_{target_var}_{ats.model}.pkl", "wb") as file:
        pickle.dump(y_preds, file)

    mae, rmse, r2 = get_mae_rmse(y_test.tolist(), y_preds)

    print(f"{ats.model} predicting {y_col}:")
    print(f"R^2: {round(r2,3)}")
    # get difference in hours instead of seconds
    print(f"MAE: {round(mae/ (60*60))} hours  = {round(mae / (60*60*24))} days")
    print(f"RMSE: {round(rmse/ (60*60))} hours  = {round(rmse / (60*60*24))} days")
