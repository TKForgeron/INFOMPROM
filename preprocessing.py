import os
import pandas as pd
import multiprocessing as mp
from pandarallel import pandarallel


ORG_DATA_DIR = "data/incidentProcess_custom.csv"
PREP_DATA_DIR = "data/preprocessed_incident_process_custom.pkl"
ALL_FEATURE_DTYPES = {
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
}  # not 100% necessary.
NAN_VALUES = [
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
    "#N/B",  # "#N/B" needed, the rest is default (also needed probably)
]


def parse_ints(df: pd.DataFrame, parallel: bool = True) -> pd.DataFrame:

    # "Handle Time (Hours)" from string to int
    def rm_comma_to_int(s: str) -> int:
        if type(s) == str:
            i = int(s.replace(",", ""))
        elif s != s:
            i = s
        return i

    if parallel:
        df["Handle Time (Hours)"] = df["Handle Time (Hours)"].parallel_apply(
            rm_comma_to_int
        )
    else:
        df["Handle Time (Hours)"] = df["Handle Time (Hours)"].apply(rm_comma_to_int)

    return df


def parse_timestamps(df: pd.DataFrame, parallel: bool = True) -> pd.DataFrame:

    # parse timestamp strings to unix timestamps (int) to save memory
    def datestr_to_unix(s: str) -> int:

        # required for parallelization in Windows, all parallel functions should be self contained due to their multiprocessing system (spawn) :(
        import datetime

        if type(s) != str:
            return s
        if (
            len(s.split("/")) > 1
        ):  # then it is of form with SLASHES instead of dashes and without microseconds
            date_format = datetime.datetime.strptime(s, "%d/%m/%Y %H:%M:%S")
        else:
            date_format = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

        return int(datetime.datetime.timestamp(date_format))

    date_cols_to_parse = [
        "ActivityTimeStamp",
        "Open Time",
        "Reopen Time",
        "Resolved Time",
        "Close Time",
    ]
    if parallel:
        df[date_cols_to_parse] = df[date_cols_to_parse].parallel_applymap(
            datestr_to_unix
        )
    else:
        df[date_cols_to_parse] = df[date_cols_to_parse].applymap(datestr_to_unix)
    return df


def do_all_preprocessing() -> None:
    if os.path.exists(ORG_DATA_DIR):
        # import data
        print(f"Importing data...")
        df = pd.read_csv(
            ORG_DATA_DIR,
            delimiter="\t",
            dtype=ALL_FEATURE_DTYPES,
            na_values=NAN_VALUES,
        )

        # preprocess in parallel
        pandarallel.initialize(verbose=0, progress_bar=False)
        print(f"Converting string timestamps to unix timestamps...")
        df = parse_timestamps(df)

        print(f"Parsing strings to integers...")
        df = parse_ints(df)

        # # <<< PURELY FOR TESTING PURPOSES

        # # preprocess single threaded
        # dfs = pd.read_csv(
        #     ORG_DATA_DIR,
        #     delimiter="\t",
        #     dtype=ALL_FEATURE_DTYPES,
        #     na_values=NAN_VALUES,
        # )
        # dfs = parse_timestamps(dfs, parallel=False)
        # dfs = parse_ints(dfs, parallel=False)

        # # if both are the same, nothing happens, else AssertionError is raised
        # assert df.equals(dfs)

        # # END OF TEST >>>

        # save/pickle
        print(f"Pickling into '{PREP_DATA_DIR}'...")
        df.to_pickle(PREP_DATA_DIR)
    else:
        current_working_dir = os.getcwd().replace("\\", "/")
        raise Exception(
            f"Cannot find the original dataset in: {current_working_dir}/{ORG_DATA_DIR}"
        )


if __name__ == "__main__":
    do_all_preprocessing()