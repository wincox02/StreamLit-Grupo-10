import streamlit as st
import pandas as pd, numpy as np
import altair as alt
import joblib, os

from src.features import add_lags

st.set_page_config(page_title="Crypto returns – DTR feedback", layout="wide")

@st.cache_resource
def load_artifact(path="models/model_feedback.pkl"):
    return joblib.load(path)

artifact = load_artifact()
model = artifact["model"]
BASE_FEATURES = artifact["base_features"]
N_LAGS = artifact["n_lags"]
scaler_y = artifact.get("scaler_y", None)
USE_FEEDBACK = artifact.get("use_feedback", True)

st.title("Predicción de % de cambio (siguiente período) – DecisionTreeRegressor con feedback")

with st.sidebar:
    st.header("Datos de entrada")
    up = st.file_uploader("Subí CSV con columnas Binance (open_time, open, high, low, close, volume, ...)", type=["csv"])
    n_recent = st.number_input("Usar últimos N registros", 200, 5000, 400, step=50)
    st.caption("Necesitamos al menos N_LAGS+1 filas para generar la próxima predicción.")

    st.divider()
    st.header("Feedback opcional (último día real)")
    last_real = st.text_input("Retorno real del último día (en %, ej: 0.8 o -1.2). Déjalo vacío si no lo tenés.")
    btn_predict = st.button("Predecir siguiente período")

def load_df(uploaded):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("Usando muestra de datos demo (data/sample_binance.csv).")
        df = pd.read_csv("data/sample_binance.csv")
    # Normalizar fecha
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

def compute_returns(df):
    df = df.copy()
    df["ret"] = df["close"].pct_change()
    return df

def next_prediction(df):
    """
    Toma el dataframe crudo con columnas Binance,
    arma lags, y predice el retorno del siguiente período.
    """
    df = compute_returns(df)
    df = add_lags(df, BASE_FEATURES, N_LAGS)

    # Última fila con lags completos para inferencia siguiente día
    X_inf = df.dropna().reset_index(drop=True)
    if len(X_inf) == 0:
        raise ValueError("No hay suficientes filas para generar lags.")

    # Features lag puras
    lag_cols = [c for c in X_inf.columns if any(c.startswith(f"{f}_lag") for f in BASE_FEATURES)]
    Xi = X_inf[lag_cols].iloc[[-1]].copy()

    # Feedback simple: si el artefacto lo usa y el usuario ingresó 'last_real'
    if USE_FEEDBACK:
        prev_pred = st.session_state.get("prev_pred_streamlit", 0.0)
        prev_real = st.session_state.get("prev_real_streamlit", 0.0)
        Xi["prev_pred"] = prev_pred
        Xi["prev_err"]  = prev_pred - prev_real
    yhat = float(model.predict(Xi)[0])

    # Actualizar estado si el usuario cargó el real del último día
    if USE_FEEDBACK and last_real.strip():
        try:
            real_pct = float(last_real.replace(",", "."))
            real = real_pct / 100.0
            st.session_state["prev_real_streamlit"] = real
            st.session_state["prev_pred_streamlit"] = yhat
        except:
            st.warning("No pude interpretar el retorno real ingresado. Usá formato numérico, ej: 0.8 ó -1.2")

    return yhat, df

df = load_df(up)

tab1, tab2 = st.tabs(["Exploración", "Predicción"])

with tab1:
    st.subheader("Exploración rápida")
    st.write("Últimas filas")
    st.dataframe(df.tail(10))
    chart = alt.Chart(df.tail(200)).mark_line().encode(
        x="date:T", y=alt.Y("close:Q", title="Close")
    ).properties(height=280)
    st.altair_chart(chart, use_container_width=True)

with tab2:
    if btn_predict:
        try:
            yhat, df_proc = next_prediction(df.tail(int(n_recent)))
            st.success(f"Predicción retorno próximo período: **{yhat*100:.3f}%**")
            # Serie para contexto
            ctx = df_proc.tail(60)[["date","close"]].copy()
            ctx["predicted_next_close"] = np.nan
            ctx.iloc[-1, ctx.columns.get_loc("predicted_next_close")] = ctx["close"].iloc[-1]*(1.0 + yhat)

            base = alt.Chart(ctx).encode(x="date:T").properties(height=280)
            real_line = base.mark_line().encode(y=alt.Y("close:Q", title="Close"))
            pred_point = base.mark_point(size=80).encode(y="predicted_next_close:Q", tooltip=["date:T","predicted_next_close:Q"])
            st.altair_chart(alt.layer(real_line, pred_point), use_container_width=True)

            st.caption("Tip: si conocés el retorno REAL del último día, cargalo en la barra lateral para alimentar prev_err.")
        except Exception as e:
            st.error(f"No pude predecir: {e}")
    else:
        st.info("Cargá un CSV o dejá el demo y presioná *Predecir*.")
