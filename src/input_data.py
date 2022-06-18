import pandas as pd
from pandasql import sqldf
from src.categorical_encoders import *
import random
import pickle


class InputData:
    def __init__(self, filename: str, sep: str = "\t", dec: str = ",") -> None:
        """Initiates the class and creates a dataframe given the filename."""

        self.df = pd.read_csv(
            "data/" + str(filename), decimal=dec, sep=sep, engine="python"
        )

    def get_df(self):
        return self.df

    def set_df(self, df):
        self.df = df

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

    def add_prev_events(self, data) -> None:

        print("Adding previous events attribute..")

        data["PrevEvents"] = data["Activity"].apply(
            lambda x: [] if pd.isnull(x) else [x]
        )
        data["PrevEvents"] = data.groupby("Incident ID")["PrevEvents"].apply(
            lambda x: x.cumsum()
        )

        return data

    def filter_incomplete_processes(self):

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

    def add_agg_col(self, aggregation: str = "rem_time") -> None:

        if aggregation == "rem_time":
            self._add_remaining_time()
        if aggregation == "rem_act":
            self._add_remaining_act()

    def save_df(
        self, out_filename: str = "converted_df", file: str = "csv", n_rows: int = -1
    ) -> None:

        print("Saving df..")
        print_df = self.df

        if n_rows >= 0:
            print_df = print_df.head(n_rows)

        if file == "csv":
            print_df.to_csv(f"data/{out_filename}.csv")

        elif file == "pickle":
            print_df.to_pickle(f"data/{out_filename}.pkl")

    def save(self, out_filename: str = "inputDataObject"):

        filehandler = open(f"data/{out_filename}.pkl", "wb")
        pickle.dump(self, filehandler)

    def apply_standard_preprocessing(
        self,
        agg_col: str,
        filter_incompletes: bool = True,
        dropna: bool = False,
        date_cols: list[str] = [],
    ) -> None:

        print("\nSTART PREPROCESSING")

        if agg_col not in ["rem_time", "rem_act"]:
            raise AssertionError("Please choose another aggregation column")

        if dropna:
            self.df = self.df.dropna(axis="index")

        if filter_incompletes:
            self.filter_incomplete_processes()

        # if "prev_events" in agg_cols:
        #     self._add_prev_events()
        if date_cols:
            self._convert_times(date_cols)

        if agg_col == "rem_time":
            self._add_remaining_time()
        if agg_col == "rem_act":
            self._add_remaining_act()

    def use_cat_encoding_on(self, encoding: str, cat_vars: list[str]):

        print(f"Encoding columns {cat_vars} using {encoding} encoding..")

        if encoding == "ohe":
            encoder = MultiOneHotEncoder(cat_vars)
        elif encoding == "label":
            encoder = MultiLabelEncoder(cat_vars)
        elif encoding == "hash":
            encoder = MultiFeatureHasher(cat_vars)
        elif encoding == "none":
            encoder = NoEncoder(cat_vars)

        self.df = encoder.fit_transform(self.df)

        # print("FINISHED PREPROCESSING\n")

    def train_test_split_on_trace(
        self, y_col: str, ratio: int = 0.8, seed: int = 42
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

        unique_ids = self.df["Incident ID"].unique().tolist()

        l = len(unique_ids)

        random.seed(seed)
        chosen_ids = random.sample(unique_ids, k=round(l * ratio))

        train_data = self.df.loc[self.df["Incident ID"].isin(chosen_ids)]
        train_Y = train_data.pop(y_col)

        test_data = self.df.loc[~self.df["Incident ID"].isin(chosen_ids)]
        test_Y = test_data.pop(y_col)

        return train_data.copy(), test_data.copy(), train_Y.copy(), test_Y.copy()
