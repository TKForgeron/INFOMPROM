import pickle
from src.ats import *
import pandas as pd
from src.print_ats import *
from src.input_data import InputData
import random
from sklearn.model_selection import train_test_split

PREPROCESSING_IN_FILE = "incidentProcess_custom.csv"
INPUTDATA_OBJECT = "preprocessed_inputData_object"
ATS_OUT_FILE = "ats"
RANDOM_SEED = 42
TARGET_COLUMN = "RemainingTime"


FILENAME = "incidentProcess_custom.csv"

DATE_COLS = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]

AGG_COLS = ["conv_time", "rem_time", "rem_act", "inc_cases", "prev_events"]


def train_test_split_on_trace(
    self,
    trace_identifier: str,
    X,
    y,
    test_size: int = None,
    train_size: int = None,
    random_state: int = None,
):
    unique_ids = self.df[trace_identifier].unique().tolist()

    pass


#     X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=RANDOM_SEED
# )

if __name__ == "__main__":

    try:
        input = pd.read_pickle(f"data/{INPUTDATA_OBJECT}.pkl")
    except:
        input = InputData(FILENAME)
        input.apply_standard_preprocessing(
            agg_col="rem_time",  # calculated y column
            filter_incompletes=True,
            date_cols=DATE_COLS,  # list of cols that must be transformed. If empty / not given, nothing will be transformed
        )

        input.use_cat_encoding_on(
            "ohe", ["Priority"]
        )  # can be a list of features that need ohe
        input.use_cat_encoding_on(
            "label", ["Category"]
        )  # can be a list of features that need label / numerical encoding
        input.use_cat_encoding_on(
            "none", ["Service Affected"]
        )  # list of features that need to be deleted

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
        model_type="avg",
        encoding_operation=None,
        seed=RANDOM_SEED,
    )

    # try:
    #     with open(f"data/{ATS_OUT_FILE}.pkl", "rb") as file:
    #         ats = pickle.load(file)
    # except:
    print("Reading ATS from pickle failed")
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
