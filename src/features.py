import pandas as pd

def add_pct_and_lags(df: pd.DataFrame, base_col: str, n_lags: int):
    out = df.copy()
    out['ret'] = out[base_col].pct_change()
    out['close_pct'] = out[base_col].pct_change()
    for l in range(1, n_lags+1):
        out[f'close_pct_lag{l}'] = out['close_pct'].shift(l)
    return out

def build_supervised(df: pd.DataFrame, feature_names):
    X = df[feature_names].dropna().reset_index(drop=True)
    y = df.loc[X.index, 'ret'].values
    return X, y
