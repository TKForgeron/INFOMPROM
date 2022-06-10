import pandas as pd
from datetime import datetime
import numpy as np

FILENAME = "incidentProcess_custom.csv"

DATE_COLS = [
    "ActivityTimeStamp",
    "Open Time",
    "Reopen Time",
    "Resolved Time",
    "Close Time",
]

AGG_COLS = [
    "conv_time",
    "rem_time",
    "rem_act"
]


class InputData():

    def __init__(self, filename: str, sep: str ='\t', dec: str=",") -> None:
        """Initiates the class and creates a dataframe given the filename."""

        self.df = pd.read_csv("data/" + str(filename),
                              decimal=dec, sep=sep, engine='python')

    def _convert_times(self, date_cols: list) -> None:

        print("Converting dates.. ")

        for col in date_cols:

            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            self.df[col] = (
                self.df[col] - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

    def _add_remaining_time(self) -> None:
        
        print("Adding remaining time attribute..")

        self.df['RemainingTime'] = self.df.groupby('Incident ID')['ActivityTimeStamp'].transform('max') - self.df['ActivityTimeStamp'] 


    def _add_remaining_act(self) -> None:

        print("Adding remaining activities attribute..")

        self.df['RemainingActivities'] = self.df.groupby('Incident ID').cumcount(ascending=False)


    def apply_preprocessing(self, agg_cols: list, date_cols: list = None) -> None:

        print("\nSTART PREPROCESSING")
                    
        if 'conv_time' in agg_cols:
            self._convert_times(date_cols)
        if 'rem_time' in agg_cols:
            self._add_remaining_time()
        if 'rem_act' in agg_cols:
            self._add_remaining_act()

        print("FINISHED PREPROCESSING\n")

    def save_df(self, name: str = 'converted_df', file: str = 'csv') -> None:
        
        print("Saving df..")

        if file == 'csv':
            self.df.to_csv('data/' + name + '.csv')

        elif file == 'pickle':
            self.df.to_pickle('data' + name + 'pkl')




if __name__ == "__main__":

    data = InputData(FILENAME)
    data.apply_preprocessing(AGG_COLS, DATE_COLS)
    data.save_df()

