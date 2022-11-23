import pandas as pd
from copy import deepcopy
from sklearn.model_selection import cross_val_score
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

# TODO fix sklearn models
# TODO make OHE cols of all activities found
# TODO predict moet per event een prediction geven
# ✓ TODO check if append() works
# TODO integrate a scoring function (e.g. MAE, MSE, Cross Entropy)
# TODO train val split
# TODO implement cross_val_score()


@dataclass(slots=True)
class Bucket:
    """
    Initializes a Bucket.

    Parameters
    ----------
        X : [list[dict]]
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

    y_col: str
    cols_to_drop: list[str]
    seed: int = 42
    cv: int = 5
    X: list[dict] = field(default_factory=list)  # becomes pd.DataFrame
    y: list[dict] = field(default_factory=list)  # becomes pd.Series
    model: Any = field(default_factory=Any)

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
