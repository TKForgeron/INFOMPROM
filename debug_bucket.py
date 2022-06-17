from src.input_data import InputData
import random
from sklearn.model_selection import train_test_split
from src.bucket import Bucket
from src.bucket_preprocessor import Preprocessor
import pandas as pd

# df = pd.read_csv("data/converted_df.csv")

# three_traces = df.iloc[:, :73]
# x_pred = df.iloc[74:75]

# bucket = Bucket(y_col="RemainingTime", data=three_traces, model_type="median")
# bucket.finalize()

# pp = Preprocessor(
#     y_col=bucket.preprocessor.y_col,
#     encoding_operation=bucket.preprocessor.encoding_operation,
# )
# three_traces = pp.prepare_for_prediction(three_traces, bucket.x_cols)

# # log = three_traces[bucket.x_cols]
# # print("-" * 10)
# # print(log)
# # print("-" * 10)

# print(f"Predicting remaining time using {bucket.model} model...")
# y_pred = bucket.model.predict(three_traces)
# print(f"Example of first 5 predictions: {y_pred[:5]}")


PREPROCESSING_IN_FILE = "incidentProcess_custom.csv"
PREPROCESSING_OUT_FILE = "preprocessed_events"
RANDOM_SEED = 42
TARGET_COLUMN = "RemainingTime"
# Some code to test the code carefully (i.e. not run it with the full event log)
# data = pd.read_csv("data/incidentProcess_custom.csv", sep="\t")

# data.to_csv("demo_data")

# data_train = data[data["Incident ID"].isin(["IM0000038", "IM0000041"])]
# data_test = data[data["Incident ID"].isin(["IM0000042"])]

# Saving time... in case you've already done the preprocessing
try:
    print("Reading preprocessed data from pickle...")
    data = pd.read_pickle(f"data/{PREPROCESSING_OUT_FILE}.pkl")
except:
    try:
        print("Reading preprocessed data from csv...")
        data = pd.read_csv(f"data/{PREPROCESSING_OUT_FILE}.csv")
    except:
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_preprocessing()
        input.save_df(PREPROCESSING_OUT_FILE, "csv")
        data = input.df


# Required input read directly from csv as lists are converted to strings.
# data["PrevEvents"] = [ast.literal_eval(x) for x in data["PrevEvents"]]

# <<<< take a sample of 5% for testing
unique_ids = data["Incident ID"].unique()


def sample_percentage(population, perc, seed):
    n_samples = int(len(population) / 100 * perc)
    random.seed(seed)
    return random.sample(population, n_samples)


sampled_ids = sample_percentage(unique_ids.tolist(), 5, RANDOM_SEED)
data = data.loc[data["Incident ID"].isin(sampled_ids)]
# remove this section for complete demo >>>>

y_col_index_no = data.columns.get_loc(TARGET_COLUMN)
X = data.iloc[:, :y_col_index_no]  # everything up to y_column
y = data.iloc[:, y_col_index_no]  # y_column

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_SEED
)

data_train = pd.concat([X_train, y_train], axis=1)

print()
print(X_train.columns.tolist())

bucket = Bucket(
    y_col=TARGET_COLUMN,
    x_cols=X_train.columns.tolist(),
    data=data_train,
    model_type="median",
)
bucket.finalize()
