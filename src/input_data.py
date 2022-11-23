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

    def _convert_times(self, date_cols: list = None) -> None:

        print("Converting dates.. ")

        if date_cols is None:
            # automatically detect and convert date columns
            for col in self.df.columns:
                if self.df[col].dtype == "object" and "time" in col.lower():
                    try:
                        self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                        self.df[col] = (
                            self.df[col] - pd.Timestamp("1970-01-01")
                        ) // pd.Timedelta("1s")
                    except ValueError:
                        pass
        else:
            # manually select and convert date columns
            for col in date_cols:

                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                self.df[col] = (
                    self.df[col] - pd.Timestamp("1970-01-01")
                ) // pd.Timedelta("1s")

    def _add_remaining_time(self) -> None:

        print("Adding remaining time attribute..")

        self.df["RemainingTime"] = (
            self.df.groupby("Incident ID")["ActivityTimeStamp"].transform("max")
            - self.df["ActivityTimeStamp"]
        )

    def _add_running_time(self) -> None:

        print("Adding running time attribute..")

        self.df["RunningTime"] = self.df["ActivityTimeStamp"] - self.df.groupby(
            "Incident ID"
        )["ActivityTimeStamp"].transform("min")

    def _add_remaining_act(self) -> None:

        print("Adding remaining activities attribute..")

        self.df["RemainingActivities"] = self.df.groupby("Incident ID").cumcount(
            ascending=False
        )

    def _add_past_act(self) -> None:

        print("Adding remaining activities attribute..")

        self.df["CurrentActivities"] = self.df.groupby("Incident ID").cumcount(
            ascending=True
        )

    def _get_list_diff(self, li1: list, li2: list) -> list:
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

    def add_prev_events(self, data) -> None:

        print("Adding previous events attribute..")

        data["PrevEvents"] = data["Activity"].apply(
            lambda x: [] if pd.isnull(x) else [x]
        )
        data["PrevEvents"] = data.groupby("Incident ID", group_keys=False)["PrevEvents"].apply(
            lambda x: x.cumsum()
        )

        return data

    def filter_incomplete_processes(self):

        print("Filtering out incomplete cases..")

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

    def filter_incomplete_processes2(self):

        print("Filtering out incomplete processes..", end="")

        df1 = self.df

        size = df1.shape[0]

        q = """
            SELECT *
            FROM df1
            WHERE  `Incident ID`  IN (SELECT `Incident ID`
                                from df1 
                                where `Incident ID` in ( select `Incident ID`  
                                                        from df1
                                                        where Activity = 'Open') 
                                    AND `Incident ID` in ( select `Incident ID`  
                                                        from df1
                                                        where activity = 'Close')
                                )
                    AND `Incident ID` NOT IN (select `Incident ID`
                                from df1 
                                where  `Incident ID` in (
                                                        select REOPEN.`Incident ID`
                                                        FROM
                                                        (select `Incident ID`,MAX(ActivityTimeStamp) AS ActivityTimeStamp,Activity
                                                        from df1
                                                        where  Activity = 'Re-open'
                                                        GROUP BY `Incident ID`,Activity) REOPEN   
                                                        JOIN
                                            (select `Incident ID`,MAX(ActivityTimeStamp) AS ActivityTimeStamp,Activity
                                            from df1
                                            where  Activity = 'Close'
                                            GROUP BY `Incident ID`,Activity) CLOSE
                                            ON REOPEN.`Incident ID`=CLOSE.`Incident ID` AND strftime(REOPEN.ActivityTimeStamp,'yyyy-mm-dd hh24:mi:ss.ff')>strftime(CLOSE.ActivityTimeStamp,'yyyy-mm-dd hh24:mi:ss.ff')
                                            ))
            """

        self.df = sqldf(q)

        print(f" [{size - self.df.shape[0]}/{size} rows deleted]")

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
        dropna: tuple[bool, int] = (False, None),
        filter_incompletes: bool = True,
        date_cols: list[str] = [],
    ) -> None:

        print("\nSTART PREPROCESSING")

        if agg_col not in ["rem_time", "rem_act"]:
            raise AssertionError("Please choose another aggregation column")

        # if dropna for rows would drop <10%, drop the NaNs here (before filter_incompletes)
        # use here ONLY for rows, otherwise apply after encoding operations

        if filter_incompletes:
            self.filter_incomplete_processes2()

        # if "prev_events" in agg_cols:
        #     self._add_prev_events()
        if date_cols == "auto":
            self._convert_times()
        elif date_cols:
            self._convert_times(date_cols)

        if agg_col == "rem_time":
            self._add_remaining_time()
        elif agg_col == "rem_act":
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

    def dropna(self, axis: int, specific_col: str = None):
        if axis not in [0, 1]:
            raise ValueError("'axis' must be either '0' or '1'")

        original_number = self.df.shape[axis]
        init_cols = self.df.columns.tolist()
        self.df = self.df.dropna(axis=axis)

        if axis == 0:

            if specific_col is not None:
                self.df = self.df.dropna(axis=0, subset=[specific_col])

            print(
                f"Dropping missing values..  [{original_number - self.df.shape[axis]}/{original_number} rows deleted]"
            )
        elif axis == 1:
            print(
                f"Dropping missing values..  [{original_number - self.df.shape[axis]}/{original_number} columns deleted]"
            )
            new_cols = self.df.columns.tolist()
            dropped_cols = self._get_list_diff(init_cols, new_cols)
            print(f"\t Deleted: {dropped_cols}")

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

    def calculate_naive_MAE(self):

        self.use_cat_encoding_on(
            "none",
            [
                "Service Affected",
                "Asset SubType Affected",
                "Service Caused",
                "Assignment Group",
                "Priority",
                "Asset Type Affected",
                "Status",
                "Closure Code",
                "Asset Caused",
                "Asset Type Caused",
                "Asset SubType Caused",
                "Asset Affected",
                "Impact",
                "Urgency",
                "Category",
                "Number of Reassignments",
                "Open Time",
                "Reopen Time",
                "Resolved Time",
                "Close Time",
                "Handle Time (Hours)",
            ],
        )

        self.filter_incomplete_processes2()

        self._convert_times(["ActivityTimeStamp"])

        self._add_remaining_time()

        self._add_running_time()

        self.df["y_time_hat"] = self.df.apply(
            lambda x: 401068.6272 - x.RunningTime, axis=1
        )

        self.df["AE_time"] = self.df.apply(
            lambda x: abs(x.y_time_hat - x.RemainingTime), axis=1
        )

        self.df["AE_time_days"] = self.df.apply(
            lambda x: abs(x.AE_time / (24 * 60 * 60)), axis=1
        )

        self._add_remaining_act()

        self._add_past_act()

        self.df["y_hat_activities"] = self.df.apply(
            lambda x: 6.547236 - x.CurrentActivities, axis=1
        )

        self.df["AE_activities"] = self.df.apply(
            lambda x: abs(x.y_hat_activities - x.RemainingActivities), axis=1
        )
