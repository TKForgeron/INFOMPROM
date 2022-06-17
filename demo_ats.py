from src.ats import *
import pandas as pd
import numpy as np
from src.print_ats import *
from src.input_data import InputData
import ast
import random
from sklearn.model_selection import train_test_split

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
        print("Reading from pickle failed -> Reading preprocessed data from csv...")
        data = pd.read_csv(f"data/{PREPROCESSING_OUT_FILE}.csv")
    except:
        print("Reading from csv failed, create data")
        input = InputData(PREPROCESSING_IN_FILE)
        input.apply_preprocessing()
        input.save_df(PREPROCESSING_OUT_FILE, "pkl")
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

# exit(0)

# data_train = data[~data["Incident ID"].isin(["IM0000042"])]
# data_test = data[data["Incident ID"].isin(["IM0000042"])]


ats = ATS(
    "Incident ID",
    "Activity",
    TARGET_COLUMN,
    "set",
    model_type="avg",
    seed=RANDOM_SEED,
)
ats.create_ATS(data_train)
ats.print()
ats.finalize()
ats.save()



# print_ATS(ats)

# i = 0

# print("\n\PREDICTION OUTPUT:\n")
# for event in data_test.to_dict(orient="records"):
#     ats.traverse_ats(event)

#     if i == 5:
#         break
#     i += 1
