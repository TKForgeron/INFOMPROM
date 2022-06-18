import pickle
from src.ats import *
import pandas as pd
from src.print_ats import *
from src.input_data import InputData
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression,
    ElasticNetCV,
)
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

PREPROCESSING_IN_FILE = "incidentProcess_custom.csv"
INPUTDATA_OBJECT = "preprocessed_inputData_object"
ATS_OUT_FILE = "ats"
RANDOM_SEED = 42
TARGET_COLUMN = "RemainingTime"
DATE_COLS = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]
AGG_COLS = ["conv_time", "rem_time", "rem_act", "inc_cases", "prev_events"]


if __name__ == "__main__":

    try:
        raise Exception(
            "Tuning preprocessing process, thus not loading pickled preprocessing instance"
        )
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}.pkl")
    except:
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_standard_preprocessing(
            agg_col="rem_time",  # calculated y column
            filter_incompletes=True,
            dropna=True,
            date_cols=DATE_COLS,  # list of cols that must be transformed. If empty / not given, nothing will be transformed
        )

        # columns that have <20 unique values are one-hot encoded
        input.use_cat_encoding_on(
            "ohe", ["Priority", "Asset Type Affected", "Status", "Closure Code"]
        )

        # columns that have have ordinal values are label encoded
        input.use_cat_encoding_on("label", ["Category"])

        # columns with too many categories are deleted
        input.use_cat_encoding_on(
            "none",
            [
                "Service Affected",
                "Asset SubType Affected",
                "Service Caused",
                "Assignment Group",
            ],
        )

        input.save_df(
            n_rows=20
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(INPUTDATA_OBJECT)

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=TARGET_COLUMN, ratio=0.05, seed=RANDOM_SEED
    )

    # X_test = input.add_prev_events(X_test)  # self explanatory

    ats = ATS(
        trace_id_col="Incident ID",
        act_col="Activity",
        representation="set",
        model=LinearRegression(),
        encoding_operation=None,
        seed=RANDOM_SEED,
    )

    try:
        raise Exception(
            "Tuning preprocessing/ATS building process, thus not loading pickled ATS instance"
        )
        with open(f"data/{ATS_OUT_FILE}.pkl", "rb") as file:
            ats = pickle.load(file)
    except:
        ats.fit(X_train, y_train)
        # ats.print()
        ats.finalize()
        ats.save(ATS_OUT_FILE)

    i = 0

    print("\nPREDICTION OUTPUT:\n")
    for event in X_test.to_dict(orient="records"):
        print(f"Prediction for {event['Incident ID'], event['Activity']}")

        # ZOU BETER ZIJN ALS IE IPV 1 EVENT INNEEMT, EEN LIJST NEEM EN LIJST VAN PREDICTIONS TERUGGEEFT
        ats.predict(event)

        if i == 5:
            break
        i += 1
