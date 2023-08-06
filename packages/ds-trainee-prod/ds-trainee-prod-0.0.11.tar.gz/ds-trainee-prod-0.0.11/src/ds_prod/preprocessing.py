from itertools import product, chain
from sklearn.model_selection import TimeSeriesSplit


class CustomValidationFolds:
    """Creates validation class that splits using moving window for the ordered dates of the data"""

    def __init__(self, **kwargs):
        self.tscv = TimeSeriesSplit(**kwargs)

    def get_n_splits(self,X=None, y=None, groups=None):
        """gets number of splits

        Yields
        ------
        n_splits: int
            number of splits
        """
        return self.tscv.get_n_splits()

    def split(self, X, y=None, groups=None):
        """ splits data X into n_splits  by time range.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data, where `n_samples` is the number of samples
            and `n_features` is the number of features.
        y : array-like of shape (n_samples,)
            Always ignored, exists for compatibility.
        groups : array-like of shape (n_samples,)
            Always ignored, exists for compatibility.
        Yields
        ------
        list of [train, test] pairs
        train : list
            The training set indices for that split.
        test : list
            The testing set indices for that split.
        """
        months = set(X.month)
        years = set(X.year)
        ym_list = list(product(years, months))[:-2]
        inds = list(self.tscv.split(ym_list))
        train_test_split = []
        train = inds[0][0]
        tr = X[X.apply(lambda x: (x[0], x[1]) in ym_list[min(train):max(train) + 1], axis=1)].index
        for i in range(0, self.get_n_splits()):
            ind = inds[i][1]
            te = X[X.apply(lambda x: (x[0], x[1]) in ym_list[min(ind):max(ind) + 1], axis=1)].index
            train_test_split.append((tr, te))
            tr = chain(tr,te)
        return train_test_split


def validation_split(X, train_ratio=0.8):
    """
    splits train X into train and validation by splitting the timeseries by the ratio

    The function takes the ordered year-months pairs from the data set, divides them
    and the dataset is divided into

    Parameters
    -------
    X: DataFrame with month and year columns
        the dataset to be divided
    train_ratio: float
        the ratio of time to go into train

    Yields
    -------
    train : list
            The training set indices for that split.
    test : list
            The testing set indices for that split.
    """
    months = set(X.month)
    years = set(X.year)
    ym_list = list(product(years, months))[:-2]
    train_num = int(train_ratio * len(ym_list))
    print(train_num)
    ind = X.apply(lambda x: (x[0], x[1]) in ym_list[:train_num], axis=1)
    train = X[ind].index
    test = X.drop(train).index
    return [train, test]
