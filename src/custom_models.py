import warnings
import pandas as pd
import copy


class AalstModel:
    def __init__(
        self,
    ) -> None:
        self.prediction = None
        self.is_custom_model = True

    def __str__(self):
        return "AalstModel()"

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit average predicting model.

        Parameters
        ----------
        X : pd.DataFrame of shape (n_samples, n_features)
            Training data.
        y : pd.Series of shape (n_samples,) or (n_samples, n_targets)
            Target values. Will be cast to X's dtype if necessary.

        Returns
        -------
        self : object
            Fitted Estimator.
        """

        self.prediction = y.mean()

        return self

    def predict(self, X: pd.DataFrame):
        if self.prediction is None:
            warnings.warn("Model has not been fitted yet")

        return [self.prediction] * X.shape[0]


class Mean(AalstModel):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def __str__(self):
        return "Mean()"

    def fit(self, X: pd.DataFrame, y: pd.Series):

        self.prediction = y.mean()

        return self


class Minimum(AalstModel):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def __str__(self):
        return "Minimum()"

    def fit(self, X: pd.DataFrame, y: pd.Series):

        self.prediction = y.min()

        return self


class Maximum(AalstModel):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def __str__(self):
        return "Maximum()"

    def fit(self, X: pd.DataFrame, y: pd.Series):

        self.prediction = y.max()

        return self


class Median(AalstModel):
    def __init__(
        self,
    ) -> None:
        super().__init__()

    def __str__(self):
        return "Median()"

    def fit(self, X: pd.DataFrame, y: pd.Series):

        self.prediction = y.median()

        return self


class Mode(AalstModel):
    def __init__(
        self,
    ) -> None:
        self.prediction = None

    def __str__(self):
        return "Mode()"

    def fit(self, X: pd.DataFrame, y: pd.Series):

        self.prediction = y.mode().tolist()
        if len(self.prediction) > 1:
            # take the middle value (floored) of the list
            self.prediction = self.prediction[len(self.prediction) // 2]
        else:
            self.prediction = self.prediction[0]

        return self


class SampleMean(AalstModel):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return "SampleMean()"

    def fit(self, X: pd.DataFrame, y: pd.Series):
        pass
        # return self
