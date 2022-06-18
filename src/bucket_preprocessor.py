import pandas as pd
import warnings


class Preprocessor:
    def __init__(
        self,
        y_col: str = None,
        encoding_operation: str = None,
    ) -> None:
        self.y_col = y_col
        self.encoding_operation = encoding_operation

    def transform_data(self, data) -> pd.DataFrame:
        # transform self.data from list of dict to df

        if type(data) == pd.DataFrame:
            warnings.warn(
                "You are trying to transform Bucket data to pd.DataFrame, but it is already a pd.DataFrame"
            )
        else:
            data = pd.DataFrame(data)
            # data = data.iloc[:, :-1]

        return data

    def encode(
        self, data, operation_type: str = None, dropna: bool = True
    ) -> pd.DataFrame:
        # check if encoding operation is specified at function call
        if operation_type == None:
            # if not, assign the encoding_operation assigned at class instantiation
            operation_type = self.encoding_operation

        if dropna:
            data = data.dropna(axis=1)

        if type(operation_type) == str:
            if operation_type.upper() == "OHE":
                pass
        else:
            # remove all non-numerical cols
            if type(data) == pd.DataFrame:
                data = data.select_dtypes(["number"])
            # elif type(data) == pd.Series:
            #     data = pd.DataFrame([data, data]).select_dtypes(["number"]).iloc[0]
            else:
                raise TypeError(
                    f"Expected pd.DataFrame (or pd.Series), got {type(data)} instead"
                )

        data_cols = data.columns.tolist()

        def get_list_diff(a: list, b: list) -> list:
            return list(set(a) - set(b)) + list(set(b) - set(a))

        x_cols = get_list_diff(data_cols, [self.y_col])

        # cumulated sum OHE
        # self.x_cols = data.columns.tolist()
        return data, x_cols

    def generate_split(
        self, data: pd.DataFrame, train_size: float = None, test_size: float = None
    ) -> tuple[pd.DataFrame, pd.Series]:

        y_col_index_no = data.columns.get_loc(self.y_col)
        X = data.iloc[:, :y_col_index_no]  # everything up to y_column
        y = data.iloc[:, y_col_index_no]  # y_column
        # NOT FINISHED YET, ADD ACTUAL TRAIN TEST SPLIT

        return X, y

    def prepare_for_prediction(
        self, x_pred: pd.DataFrame, training_x_cols: list[str]
    ) -> pd.DataFrame:

        x_pred = pd.DataFrame(x_pred)
        x_pred = x_pred[training_x_cols]

        return x_pred
