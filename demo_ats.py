import pickle
from src.ats import *
import pandas as pd
from src.print_ats import *
from src.input_data import InputData
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from src.metrics import get_mae_mse
from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
    ElasticNetCV,
)
from sklearn.svm import SVR
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from src.helper import print_progress_bar
from src.globals import (
    PREPROCESSING_IN_FILE,
    INPUTDATA_OBJECT,
    ATS_OUT_FILE,
    RANDOM_SEED,
    TARGET_COLUMN,
    DATE_COLS,
)


if __name__ == "__main__":

    try:
        raise Exception("tuning data prepprocessing step")
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}.pkl")
    except:
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_standard_preprocessing(
            agg_col="rem_time",  # calculated y column
            dropna=(True, 0),
            filter_incompletes=True,
            date_cols="auto"
            # date_cols=DATE_COLS,  # when list passed: those cols will be transformed, when empty: nothing will be transformed, when 'auto' passed: will automatically detect date cols and transform them
        )

        # columns that have <20 unique values are one-hot encoded
        input.use_cat_encoding_on(
            "ohe", ["Priority", "Asset Type Affected", "Status", "Closure Code"]
        )

        # # columns that have have ordinal values are label encoded
        input.use_cat_encoding_on("label", ["Category"])

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

        # print(input.get_df().head(2))
        # exit(0)

        print("\t counting NaNs in 'Incident ID'.. ")
        test_df = input.get_df().iloc[:, 0:2]
        print(f"\t {test_df}")
        init_shape = test_df.shape
        print(f"\t {init_shape}")
        test_df.dropna(axis=0, inplace=True)
        print(f"\t {test_df.shape}")
        print(f"\t dropped: {init_shape[0]-test_df.shape[0]}")
        print()
        exit(0)

        # drop missing values, as most models don't accept this
        # we drop per column, as then only 4 will be lost
        input.dropna(axis=1)

        input.save_df(
            n_rows=20
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(INPUTDATA_OBJECT)

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=TARGET_COLUMN, ratio=0.8, seed=RANDOM_SEED
    )

    print(
        f"xtrain: {X_train.shape}, xtest:{X_test.shape}, ytrain:{y_train.shape}, ytest: {y_test.shape}"
    )

    X_test = input.add_prev_events(X_test)

    df = input.get_df()
    print(df.describe)

    print(f"training cols: {X_train.columns}")

    exit(0)
    # IF ATS ALREADY BUILT
    # with open(f"data/{ATS_OUT_FILE}.pkl", "rb") as file:
    #     ats = pickle.load(file)

    ats = ATS(
        trace_id_col="Incident ID",
        act_col="Activity",
        y_col="RemainingTime",
        representation="multiset",
        horizon=1,
        model=LinearRegression(),
        seed=RANDOM_SEED,
    )

    ats.fit(X_train, y_train)
    ats.finalize()
    # ats.print()

    ats.save(ATS_OUT_FILE)

print_progress_bar(0, len(y_test), prefix="Prediction:", suffix="Complete", length=50)

y_preds = []

for i, event in enumerate(X_test.to_dict(orient="records")):

    y_preds.append(ats.predict(event))
    print_progress_bar(
        i + 1, len(y_test), prefix="Prediction:", suffix="Complete", length=50
    )


# pickling y_test
with open("data/y_test.pkl", "wb") as file:
    pickle.dump(y_test, file)

# pickling all predicted values into a pickled variable with name of the model used
with open(f"data/y_preds_{ats.model}.pkl", "wb") as file:
    pickle.dump(y_preds, file)


mae, mse = get_mae_mse(y_test.tolist(), y_preds)

print(ats.model)
print(
    f"MAE: {round(mae/ (60*60))} hours  = {round(mae / (60*60*24))} days"
)  # get difference in hours instead of seconds
print(
    f"MSE: {round(mse/ (60*60))} hours  = {round(mse / (60*60*24))} days"
)  # get difference in hours instead of seconds
