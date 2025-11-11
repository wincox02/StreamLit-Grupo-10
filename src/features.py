import pandas as pd
import numpy as np

def add_pct_and_lags(df: pd.DataFrame, base_col: str, n_lags: int):
    """
    Agrega todas las características necesarias para el modelo:
    - Retornos porcentuales de OHLCV
    - Lags de close_pct
    - Medias móviles (3, 7, 14)
    - Volatilidad (7, 14)
    - Momentum (3, 7)
    - RSI (14)
    """
    out = df.copy()
    
    # Retornos porcentuales
    out['ret'] = out[base_col].pct_change()
    out['close_pct'] = out[base_col].pct_change()
    
    # Retornos de OHLC si existen
    if 'open' in out.columns:
        out['open_pct'] = out['open'].pct_change()
    if 'high' in out.columns:
        out['high_pct'] = out['high'].pct_change()
    if 'low' in out.columns:
        out['low_pct'] = out['low'].pct_change()
    if 'volume' in out.columns:
        out['volume_pct'] = out['volume'].pct_change()
    
    # Lags de close_pct
    for l in range(1, n_lags+1):
        out[f'close_pct_lag{l}'] = out['close_pct'].shift(l)
    
    # Medias móviles
    out["ma3"] = out["close_pct"].rolling(3).mean()
    out["ma7"] = out["close_pct"].rolling(7).mean()
    out["ma14"] = out["close_pct"].rolling(14).mean()
    
    # Volatilidad
    out["volatilidad_7"] = out["close_pct"].rolling(7).std()
    out["volatilidad_14"] = out["close_pct"].rolling(14).std()
    
    # Momentum
    out["momentum_3"] = out["close_pct"] - out["close_pct"].shift(3)
    out["momentum_7"] = out["close_pct"] - out["close_pct"].shift(7)
    
    # RSI (Relative Strength Index)
    delta = out["close_pct"]
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)  # Evitar división por cero
    out["rsi_14"] = 100 - (100 / (1 + rs))
    
    return out

def build_supervised(df: pd.DataFrame, feature_names):
    X = df[feature_names].dropna().reset_index(drop=True)
    y = df.loc[X.index, 'ret'].values
    return X, y
