# External imports
import pickle
import pandas as pd
from sklearn.linear_model import (
    LinearRegression,  # linear, no outliers in data, no correlation between features
)
from sklearn.neighbors import (
    KNeighborsRegressor,  # MAE: 46
    # RadiusNeighborsRegressor,
)  # nonlinear, many features, few important features, sample/feature ratio: high sample
from sklearn.svm import (
    SVR,  # nonlinear, many features, outliers in data, few important features, sample/feature ratio: high feature (TAKES VEEERY LONG)
)
from sklearn.ensemble import (
    HistGradientBoostingRegressor,  # nonlinear, <10 features, no noise/outliers, >10000 samples, robust against missing values
    BaggingRegressor,
    # RandomForestRegressor,
    # AdaBoostRegressor,
)

# Internal imports
from src.ats import *
from src.print_ats import *
from src.input_data import InputData
from src.custom_models import Mean, Median, Mode  # , Minimum, Maximum, SampleMean
from src.metrics import get_mae_rmse
from src.helper import print_progress_bar
from src.globals import (
    PREPROCESSING_IN_FILE,
    INPUTDATA_OBJECT,
    BASE_ATS_OUT_FILE,
    RANDOM_SEED,
    TARGET_VARS,
    TIME_TARGET_COLUMN,
    ACTIVITY_TARGET_COLUMN,
)


if __name__ == "__main__":

    y_cols = [TIME_TARGET_COLUMN, ACTIVITY_TARGET_COLUMN]
    models = [
        # Mean(),
        # Median(),
        # Mode(),
        # LinearRegression(),
        # SVR(),
        # KNeighborsRegressor(n_jobs=8),
        HistGradientBoostingRegressor(random_state=RANDOM_SEED, warm_start=True),
        # BaggingRegressor(random_state=RANDOM_SEED, n_jobs=8),
    ]
    representations = ["multiset"]  # , 'set', "trace"]
    horizons = [1]  # [1, 2, 4, 8] # 2 works worse, 5 even worse
    print(
        f"Looping through: {y_cols}, {models}, {representations}, and horizons: {horizons}"
    )

    for target_var, y_col in zip(TARGET_VARS, y_cols):
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

        for model in models:
            for representation in representations:
                for horizon in horizons:

                    # If ATS already fitted (not finalized)
                    try:
                        with open(
                            f"data/{BASE_ATS_OUT_FILE}_{target_var}.pkl", "rb"
                        ) as file:
                            ats = pickle.load(file)
                    except:
                        pass

                    ats = ATS(
                        case_id_col="Incident ID",
                        act_col="Activity",
                        y_col=y_col,
                        representation=representation,
                        horizon=horizon,
                        seed=RANDOM_SEED,
                    )
                    ats.fit(X_train, y_train)
                    ats.save(f"{BASE_ATS_OUT_FILE}_{target_var}")

                    ats.finalize(model=model)

                    print_progress_bar(
                        0,
                        len(y_test),
                        prefix="Prediction:",
                        suffix="Complete",
                        length=50,
                    )

                    y_preds = []

                    for i, event in enumerate(X_test.to_dict(orient="records")):

                        y_preds.append(ats.predict(event))
                        print_progress_bar(
                            i + 1,
                            len(y_test),
                            prefix="Prediction:",
                            suffix="Complete",
                            length=50,
                        )

                    # pickling all predicted values into a pickled variable with name of the model used
                    with open(
                        f"data/y_preds_{target_var}_{ats.model}_horizon{horizon}_{representation}.pkl",
                        "wb",
                    ) as file:
                        pickle.dump(y_preds, file)

                    mae, rmse, r2 = get_mae_rmse(y_test.tolist(), y_preds)

                    print(f"{ats.model} predicting {y_col}:")
                    print(f"R^2: {round(r2,3)}")

                    if "time" in target_var:
                        # get difference in hours instead of seconds
                        print(
                            f"MAE: {round(mae/ (60*60))} hours  = {round(mae / (60*60*24))} days"
                        )
                        print(
                            f"RMSE: {round(rmse/ (60*60))} hours  = {round(rmse / (60*60*24))} days"
                        )
                    else:
                        print(f"MAE: {round(mae,2)} activities")
                        print(f"RMSE: {round(rmse,2)} activities")

    # # wrapping all results in csv per TARGET_VAR
    # df = pd.DataFrame()

    # for target_var in TARGET_VARS:
    #     for model in models:
    #         for horizon in horizons:
    #             for representation in representations:
    #                 y_preds = pd.read_pickle(
    #                     f"data/y_preds_{target_var}_{model}_horizon{horizon}_{representation}.pkl"
    #                 )
    #                 df_y_preds_col = pd.DataFrame({f"{target_var}_{model}": y_preds})
    #                 df = pd.concat([df, df_y_preds_col], axis=1)

    #     y_test = pd.read_pickle(f"data/y_test_{target_var}.pkl")
    #     df_y_test_col = pd.DataFrame({f"{target_var}": y_preds})
    #     df = pd.concat([df, df_y_test_col], axis=1)

    # df_rem_time = df.loc[:, : TARGET_VARS[0]]
    # df_rem_act = df.loc[:, TARGET_VARS[0] : TARGET_VARS[1]].iloc[:, 1:]

    # df_rem_time.to_csv(f"results/{TARGET_VARS[0]}.csv")
    # df_rem_act.to_csv(f"results/{TARGET_VARS[1]}.csv")
