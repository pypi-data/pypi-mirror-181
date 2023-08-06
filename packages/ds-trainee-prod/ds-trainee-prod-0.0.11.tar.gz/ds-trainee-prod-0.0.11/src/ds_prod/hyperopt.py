from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from src.ds_prod.preprocessing import validation_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np


class HOpt:
    def __init__(self, x, y, val_split=0.8):
        [tr, te] = validation_split(x, val_split)
        self.X_train = x.iloc[tr]
        self.X_val = x.iloc[te]
        self.Y_train = y.iloc[tr]
        self.Y_val = y.iloc[te]
        self.space = {
            'n_estimators': hp.randint('n_estimators', 50, 200),
            'learning_rate': hp.choice('learning_rate', np.arange(0.01, 0.1, 0.01)),
            'max_depth': hp.choice('max_depth', np.arange(5, 8, 1, dtype=int)),
            'min_child_weight': hp.choice('min_child_weight', np.arange(0, 8, 1, dtype=int))
        }

    def get_space(self):
        return self.space

    def set_space(self, newspace):
        self.space = newspace

    def f(self, params):
        xgb1 = XGBRegressor(tree_method='gpu_hist', **params)
        xgb1.fit(self.X_train, self.Y_train)
        y_pred = xgb1.predict(self.X_val)
        acc = mean_squared_error(self.Y_val, y_pred)
        return {'loss': acc, 'status': STATUS_OK}

    def optimize(self, evals=50):
        trials = Trials()
        best = fmin(fn=self.f, space=self.space, algo=tpe.suggest,
                    trials=trials,
                    max_evals=evals)
        return [best, trials]
