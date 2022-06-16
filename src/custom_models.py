import warnings
import pandas as pd


class Sample_mean:
    def __init__(self) -> None:
        pass

    def fit():
        """
        Fit sample mean predicting model.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,) or (n_samples, n_targets)
            Target values. Will be cast to X's dtype if necessary.

        Returns
        -------
        self : object
            Fitted Estimator.
        """
        pass

    def train(self):
        self.fit()

    def predict():
        warnings.warn("Sample mean not yet implemented")
        pass


class Average:
    def __init__(
        self,
    ) -> None:
        self.prediction = None

    def __str__(self):
        return "Average()"

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

    def train(self):
        return self.fit()

    def predict(self, X: pd.DataFrame):
        if not self.prediction:
            warnings.warn("Model has not been fitted yet")
        return [self.prediction] * X.shape[0]


class Minimum:
    def __init__(
        self,
    ) -> None:
        self.prediction = None

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

        self.prediction = y.min()

        return self

    def train(self):
        return self.fit()

    def predict(self, X: pd.DataFrame):
        if not self.prediction:
            warnings.warn("Model has not been fitted yet")
        return [self.prediction] * X.shape[0]


class Maximum:
    def __init__(
        self,
    ) -> None:
        self.prediction = None

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

        self.prediction = y.max()

        return self

    def train(self):
        return self.fit()

    def predict(self, X: pd.DataFrame):
        if not self.prediction:
            warnings.warn("Model has not been fitted yet")
        return [self.prediction] * X.shape[0]


class Median:
    def __init__(
        self,
    ) -> None:
        self.prediction = None

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

        self.prediction = y.median()

        return self

    def train(self):
        return self.fit()

    def predict(self, X: pd.DataFrame):
        if not self.prediction:
            warnings.warn("Model has not been fitted yet")
        return [self.prediction] * X.shape[0]


class Mode:
    def __init__(
        self,
    ) -> None:
        self.prediction = None

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

        self.prediction = y.mode()

        return self

    def train(self):
        return self.fit()

    def predict(self, X: pd.DataFrame):
        if not self.prediction:
            warnings.warn("Model has not been fitted yet")
        return [self.prediction] * X.shape[0]
