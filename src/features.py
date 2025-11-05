import pandas as pd

def add_lags(df, feature_cols, n_lags):
    out=df.copy()
    for c in feature_cols:
        for l in range(1,n_lags+1):
            out[f"{c}_lag{l}"]=out[c].shift(l)
    return out
