import pandas as pd

def add_lags(df, feature_cols, n_lags):
    out = df.copy()
    for c in feature_cols:
        for l in range(1, n_lags+1):
            out[f"{c}_lag{l}"] = out[c].shift(l)
    return out

def prepare_supervised(df, feature_cols, n_lags):
    X = add_lags(df, feature_cols, n_lags)
    X = X.dropna().reset_index(drop=True)
    # solo columnas lag:
    lag_cols = [c for c in X.columns for f in feature_cols if c.startswith(f"{f}_lag")]
    return X, lag_cols
