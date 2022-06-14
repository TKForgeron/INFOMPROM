import pandas as pd
from datetime import datetime
import numpy as np
from pandasql import sqldf

FILENAME = "incidentProcess_custom.csv"

DATE_COLS = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]

AGG_COLS = ["conv_time", "rem_time", "rem_act", "inc_cases", "prev_events"]


class InputData:
    def __init__(self, filename: str, sep: str = "\t", dec: str = ",") -> None:
        """Initiates the class and creates a dataframe given the filename."""

        self.df = pd.read_csv(
            "data/" + str(filename), decimal=dec, sep=sep, engine="python"
        )

    def _convert_times(self, date_cols: list) -> None:

        print("Converting dates.. ")

        for col in date_cols:

            self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
            self.df[col] = (self.df[col] - pd.Timestamp("1970-01-01")) // pd.Timedelta(
                "1s"
            )

    def _add_remaining_time(self) -> None:

        print("Adding remaining time attribute..")

        self.df["RemainingTime"] = (
            self.df.groupby("Incident ID")["ActivityTimeStamp"].transform("max")
            - self.df["ActivityTimeStamp"]
        )

    def _add_remaining_act(self) -> None:

        print("Adding remaining activities attribute..")

        self.df["RemainingActivities"] = self.df.groupby("Incident ID").cumcount(
            ascending=False
        )

    def _add_prev_events(self) -> None:

        print("Adding previous events attribute..")

        self.df["PrevEvents"] = self.df["Activity"].apply(
            lambda x: [] if pd.isnull(x) else [x]
        )
        self.df["PrevEvents"] = self.df.groupby("Incident ID")["PrevEvents"].apply(
            lambda x: x.cumsum()
        )

    def _filter_incomplete_processes(self):

        print("Filtering out incomplete processes..")

        df1 = self.df
        q = """
            select *
            from df1 
            where `Incident ID` in (  select `Incident ID`  
                                    from df1
                                    where Activity = 'Open')
                                    AND `Incident ID` in
                                    ( select`Incident ID` 
                                    from df1
                                    where Activity = 'Close')
        """
        self.df = sqldf(q)

<<<<<<< HEAD
<<<<<<< HEAD

    def apply_preprocessing(self, agg_cols: list = AGG_COLS, date_cols: list = DATE_COLS) -> None:
=======
=======
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0
    def apply_preprocessing(self, agg_cols: list, date_cols: list = None) -> None:
>>>>>>> ed9eb8b14fa5cf882e64d0ca9c3c7ff119ed63b0

        print("\nSTART PREPROCESSING")

        if "inc_cases" in agg_cols:
            self._filter_incomplete_processes()
        if "prev_events" in agg_cols:
            self._add_prev_events()
        if "conv_time" in agg_cols:
            if not date_cols:
                raise AssertionError(
                    "ERROR: No columns for date conversions were given!"
                )
            self._convert_times(date_cols)
        if "rem_time" in agg_cols:
            self._add_remaining_time()
        if "rem_act" in agg_cols:
            self._add_remaining_act()

        print("FINISHED PREPROCESSING\n")

    def save_df(self, name: str = "converted_df", file: str = "csv") -> None:

        print("Saving df..")

        if file == "csv":
            self.df.to_csv("data/" + name + ".csv")

        elif file == "pickle":
            self.df.to_pickle("data" + name + "pkl")


if __name__ == "__main__":

    input = InputData(FILENAME)
    input.apply_preprocessing(AGG_COLS, DATE_COLS)
    # input.filter_incomplete_processes()
    input.save_df()
