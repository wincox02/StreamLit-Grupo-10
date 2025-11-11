import streamlit as st
import pandas as pd, numpy as np
import altair as alt
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from src.features import add_pct_and_lags, build_supervised

st.set_page_config(page_title="DTR – Entrena y Predice en vivo", layout="wide")
st.title("DecisionTreeRegressor – Entrenamiento en la app + Predicción")

N_LAGS_DEFAULT = 5
BASE_FEATURES = ['close']  # usamos retornos de close (close_pct + lags)

# Feature names completas (las mismas que usa el modelo guardado)
def get_feature_names(n_lags, include_volume=False):
    """Retorna la lista completa de características que usa el modelo"""
    feature_cols = [
        "open_pct", "high_pct", "low_pct", "close_pct",
        "ma3", "ma7", "ma14",
        "volatilidad_7", "volatilidad_14",
        "momentum_3", "momentum_7", "rsi_14"
    ]
    if include_volume:
        feature_cols.append("volume_pct")
    # Agregar lags
    feature_cols += [f"close_pct_lag{k}" for k in range(1, n_lags+1)]
    return feature_cols

@st.cache_data(show_spinner=False)
def load_csv(uploaded):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("data/sample_binance.csv")
    # normalizar fecha
    if "open_time" in df.columns:
        if np.issubdtype(type(df["open_time"].iloc[0]), np.integer):
            df["date"] = pd.to_datetime(df["open_time"], unit="ms")
        else:
            df["date"] = pd.to_datetime(df["open_time"])
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        raise ValueError("No encuentro 'open_time' o 'date' en el CSV.")
    return df.sort_values("date").reset_index(drop=True)

def train_model(df, n_lags, min_train=300, random_state=42, include_volume=False):
    # Construir features: todas las características técnicas
    df_feat = add_pct_and_lags(df, base_col="close", n_lags=n_lags)
    feature_names = get_feature_names(n_lags, include_volume=include_volume)
    
    X, y = build_supervised(df_feat, feature_names)
    if len(X) < min_train:
        min_train = max(50, int(len(X) * 0.7))

    # Entrenamiento simple (fit a todo el histórico salvo la última fila para tener test mínimo)
    split = max(min_train, len(X)-1)
    Xtr, ytr = X.iloc[:split], y[:split]
    Xte, yte = X.iloc[split:], y[split:]

    reg = DecisionTreeRegressor(random_state=random_state, min_samples_leaf=5)
    reg.fit(Xtr, ytr)

    # Métricas
    if len(Xte) > 0:
        yhat = reg.predict(Xte)
        mae  = mean_absolute_error(yte, yhat)
        mse  = mean_squared_error(yte, yhat)
        rmse = np.sqrt(mse)
        r2   = r2_score(yte, yhat) if len(yte)>1 else float("nan")
    else:
        mae = mse = rmse = r2 = float("nan")

    artifact = {
        "model": reg,
        "feature_names": feature_names,
        "n_lags": n_lags,
        "base_features": BASE_FEATURES,
        "include_volume": include_volume,
    }
    return artifact, {"mae": mae, "rmse": rmse, "r2": r2}, df_feat

with st.sidebar:
    st.header("Datos")
    up = st.file_uploader("CSV Binance (open_time, open, high, low, close, volume...)", type=["csv"])
    n_lags = st.number_input("N° de lags de retornos (close_pct)", 2, 20, N_LAGS_DEFAULT, 1)
    btn_train = st.button("Entrenar modelo")

df = load_csv(up)

tab1, tab2, tab3 = st.tabs(["Explorar", "Entrenar", "Predecir"])

with tab1:
    st.subheader("Exploración")
    st.write(df.tail(8))
    st.altair_chart(
        alt.Chart(df.tail(300)).mark_line().encode(x="date:T", y=alt.Y("close:Q", title="Close")).properties(height=280),
        use_container_width=True
    )

with tab2:
    st.subheader("Entrenamiento")
    if btn_train:
        # Verificar si tenemos columna de volumen
        has_volume = "volume" in df.columns
        artifact, metrics, df_feat = train_model(df, int(n_lags), include_volume=has_volume)
        st.session_state["artifact"] = artifact
        st.session_state["df_train"] = df_feat
        st.success(f"Entrenado. MAE={metrics['mae']:.6f} | RMSE={metrics['rmse']:.6f} | R2={metrics['r2']:.4f}")
        st.caption("El modelo usa retornos de OHLCV, medias móviles, volatilidad, momentum, RSI y lags.")
        with st.expander("Ver características del modelo"):
            st.write("Features:", artifact["feature_names"])
    else:
        st.info("Ajustá N° de lags y presioná **Entrenar modelo**.")

with tab3:
    st.subheader("Predicción del siguiente período")
    if "artifact" not in st.session_state:
        st.warning("Primero entrená el modelo en la pestaña **Entrenar**.")
    else:
        # Inputs de un nuevo día (OHLCV)
        st.write("Ingresá el **nuevo día** (se agregará al histórico para formar los lags):")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_open = st.number_input("Open", value=float(df["open"].iloc[-1]), format="%.6f")
            new_high = st.number_input("High", value=float(df["high"].iloc[-1]), format="%.6f")
        with col2:
            new_low  = st.number_input("Low", value=float(df["low"].iloc[-1]), format="%.6f")
            new_close= st.number_input("Close", value=float(df["close"].iloc[-1]), format="%.6f")
        with col3:
            new_vol  = st.number_input("Volume", value=float(df["volume"].iloc[-1]), format="%.6f")

        if st.button("Predecir próximo retorno (%)"):
            try:
                # 1) Append new row to last date+1
                df_new = df.copy()
                next_date = df_new["date"].iloc[-1] + pd.Timedelta(days=1)
                row = {
                    "symbol": df_new["symbol"].iloc[-1] if "symbol" in df_new.columns else "ASSET",
                    "interval": df_new["interval"].iloc[-1] if "interval" in df_new.columns else "1d",
                    "open_time": int(next_date.value/1e6),
                    "open": new_open, "high": new_high, "low": new_low, "close": new_close, "volume": new_vol,
                    "date": next_date,
                }
                df_new = pd.concat([df_new, pd.DataFrame([row])], ignore_index=True)

                # 2) Rebuild features and take last row
                n_lags = st.session_state["artifact"]["n_lags"]
                df_feat = add_pct_and_lags(df_new, base_col="close", n_lags=n_lags)
                fnames = st.session_state["artifact"]["feature_names"]
                
                # Verificar que todas las características existen
                missing_features = [f for f in fnames if f not in df_feat.columns]
                if missing_features:
                    st.error(f"❌ Faltan características en los datos: {missing_features}")
                    st.warning("⚠️ El modelo fue entrenado con características diferentes. Por favor, entrena un nuevo modelo en la pestaña 'Entrenar'.")
                    st.stop()
                
                Xi = df_feat[fnames].dropna().reset_index(drop=True).iloc[[-1]]
                
                if len(Xi) == 0:
                    st.error("❌ No hay suficientes datos históricos para generar las características necesarias.")
                    st.info("Se necesitan al menos 14 períodos históricos para calcular todas las características (medias móviles, RSI, etc.)")
                    st.stop()

                # 3) Predict
                model = st.session_state["artifact"]["model"]
                yhat = float(model.predict(Xi)[0])
                st.success(f"Predicción retorno próximo período: **{yhat*100:.3f}%**")

                # Contexto visual
                ctx = df_new.tail(60)[["date","close"]].copy()
                ctx["predicted_next_close"] = np.nan
                ctx.iloc[-1, ctx.columns.get_loc("predicted_next_close")] = ctx["close"].iloc[-1]*(1.0 + yhat)
                base = alt.Chart(ctx).encode(x="date:T").properties(height=300)
                st.altair_chart(alt.layer(
                    base.mark_line().encode(y=alt.Y("close:Q", title="Close")),
                    base.mark_point(size=80).encode(y="predicted_next_close:Q", tooltip=["date:T","predicted_next_close:Q"])
                ), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error en la predicción: {str(e)}")
                st.warning("⚠️ Si estás usando un modelo previamente guardado, por favor entrena un nuevo modelo en la pestaña 'Entrenar'.")
