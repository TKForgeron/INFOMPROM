import pandas as pd
import datetime

dtypes = {
    "Incident ID": str,
    "Activity": str,
    "ActivityTimeStamp": str,
    "Asset Affected": str,
    "Asset Type Affected": str,
    "Asset SubType Affected": str,
    "Service Affected": str,
    "Status": str,
    "Impact": int,
    "Urgency": int,
    "Priority": int,
    "Category": str,
    "Number of Reassignments": float,
    "Open Time": str,
    "Reopen Time": str,
    "Resolved Time": str,
    "Close Time": str,
    "Handle Time (Hours)": str,
    "Closure Code": str,
    "Asset Caused": str,
    "Asset Type Caused": str,
    "Asset SubType Caused": str,
    "Service Caused": str,
    "Assignment Group": str,
}

df = pd.read_csv(
    "data/incidentProcess_custom.csv",
    delimiter="\t",
    dtype=dtypes,
    na_values=[
        "#N/A",
        "#N/A N/A",
        "#NA",
        "-1.#IND",
        "-1.#QNAN",
        "-NaN",
        "-nan",
        "1.#IND",
        "1.#QNAN",
        "<NA>",
        "N/A",
        "NA",
        "NULL",
        "NaN",
        "n/a",
        "nan",
        "null",
        "#N/B",
    ],
)


def datestr_to_unix(s):
    if type(s) != str:
        return s
    if (
        len(s.split("/")) > 1
    ):  # then it is of form with SLASHES instead of dashes and without microseconds
        date_format = datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S")
    else:
        date_format = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

    return datetime.datetime.timestamp(date_format)


date_cols_to_parse = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]

df[date_cols_to_parse] = df[date_cols_to_parse].applymap(datestr_to_unix)
df.to_pickle("./data/preprocessed_incident_process_custom.pkl")
