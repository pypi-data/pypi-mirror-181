import pandas as pd


def feature_importance(X, model):
    feat_imp = pd.DataFrame({"columns": X.columns, "feature_importance": model.feature_importances_})
    return feat_imp


def drop_irrelevant_features(X, feat_imp, thresh=1e-5):
    cols = feat_imp[feat_imp.feature_importance < thresh].columns
    return X.drop(columns=cols)
