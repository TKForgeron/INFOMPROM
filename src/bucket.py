import pandas as pd
from copy import deepcopy
from sklearn.model_selection import cross_val_score
from copy import deepcopy


class Bucket:
    # TODO fix sklearn models
    # TODO make OHE cols of all activities found
    # TODO predict moet per event een prediction geven
    # ✓ TODO check if append() works
    # TODO integrate a scoring function (e.g. MAE, MSE, Cross Entropy)
    # TODO train val split
    # TODO implement cross_val_score()

    def __init__(
        self,
        y_col: str,
        cols_to_drop: list[str],
        # model,
        seed: int = None,
        cv: int = None,
    ) -> None:
        """
        Initializes a Bucket.

        Parameters
        ----------
            data : [list[dict]]
                A subset of a complete event log, filtered by states using
                an Annotated Transition System.
                At initialization (in an ATS node) this is a list of dictionaries.
            y_col : [str]
                Column name of the target variable.
            model : {Some estimator}
                Estimator class that is passed. This class must have the methods:
                fit() and predict().
            seed : [int]
                Controls the randomness that some models can have.
            cv : [int]
                Determines the number of folds used in the cross-validation process.

        """

        self.y_col = y_col
        self.X = []  # becomes pd.DataFrame
        self.y = []  # becomes pd.Series
        self.cols_to_drop = cols_to_drop

        # self.model = deepcopy(model)
        if seed is None:
            seed = 42
        if cv is None:
            cv = 5
        self.cv = cv
        self.mean_accuracy = None  # float

    def append(self, x_labels: dict, y_val: int) -> None:

        self.X.append(x_labels)
        self.y.append(y_val)

    def predict(self, pred_x: pd.DataFrame) -> list[float]:

        x_cols = self.X.columns.tolist()
        pred_x = pred_x[x_cols]
        return self.model.predict(pred_x)

    def predict_one(self, pred_x) -> float:

        formatted_x = pd.DataFrame([pred_x])
        return self.predict(formatted_x)[0]

    def finalize(self, model) -> None:

        self.X = pd.DataFrame(self.X).drop(self.cols_to_drop, axis=1)
        self.y = pd.Series(self.y)
        self.y.name = self.y_col

        self.model = deepcopy(model)
        self.model.fit(self.X, self.y)
