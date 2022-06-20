from src.bucket import Bucket
from src.print_ats import *
from src.input_data import InputData
import pandas as pd
from src.custom_models import Average, Minimum, Maximum, SampleMean, Median, Mode
from sklearn.linear_model import (
    HuberRegressor,
    LassoLarsCV,
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
            n_rows=50
        )  # save function with new "n_rows" feature that ensures opening in vscode

        input.save(INPUTDATA_OBJECT)

    # split function that keeps traces together
    X_train, X_test, y_train, y_test = input.train_test_split_on_trace(
        y_col=TARGET_COLUMN, ratio=0.1, seed=RANDOM_SEED
    )

    X_test = input.add_prev_events(X_test)  # self explanatory

    bucket = Bucket(
        id=1,
        x_cols=X_train.columns.tolist(),
        y_col=y_train.name,
        data=pd.concat([X_train, y_train], axis=1),
        model=LinearRegression(),
    )
    bucket.finalize()
    # y_pred = bucket.predict(X_test)
    # print(y_pred[:5])








    # Nodig voor ATS of preprocessing:
    # Incident ID
    # Activity
    # PrevEvents, if still exists after bucket._transform_data()

    # Nuttig voor one-hot encoding:
    # Asset Type Affected
    # Status
    # Closure Code

    # Nuttig voor hash encoding:
    # Asset SubType Affected
    # Service Caused
    # Assignment Group
