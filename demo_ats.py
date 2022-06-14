from src.ats import *
import pandas as pd
import numpy as np
from src.print_ats import *
from src.input_data import InputData
import ast

FILENAME = "incidentProcess_custom.csv"

# Some code to test the code carefully (i.e. not run it with the full event log)
# data = pd.read_csv("data/incidentProcess_custom.csv", sep="\t")

# data.to_csv("demo_data")

# data_train = data[data["Incident ID"].isin(["IM0000038", "IM0000041"])]
# data_test = data[data["Incident ID"].isin(["IM0000042"])]


input = InputData(FILENAME)
input.apply_preprocessing()
input.save_df()

data = input.df

# Required input read directly from csv as lists are converted to strings.
# data["PrevEvents"] = [ast.literal_eval(x) for x in data["PrevEvents"]]

data_train = data[~data["Incident ID"].isin(["IM0000042"])]
data_test = data[data["Incident ID"].isin(["IM0000042"])]


ats = ATS("Incident ID", "Activity", "RemainingTime", "set")
ats.create_ATS(data_train)
ats.print()
ats.finalize()

# print_ATS(ats)

i = 0 

print("\n\PREDICTION OUTPUT:\n")
for event in data_test.to_dict(orient="records"):
    ats.traverse_ats(event)

    if i == 5:
        break
    i +=1
