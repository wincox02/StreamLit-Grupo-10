import streamlit as st
import pandas as pd, numpy as np
import altair as alt
import joblib
from src.features import add_lags

st.set_page_config(page_title="Crypto returns – DTR feedback", layout="wide")

@st.cache_resource
def load_artifact(path="models/model_feedback.pkl"):
    return joblib.load(path)

def ensure_feature_names(df_raw, feature_names, base_features, n_lags, use_feedback=True):
    df = df_raw.copy()
    # close_pct and lags if needed
    if any(name.startswith("close_pct") for name in feature_names):
        df["close_pct"] = df["close"].pct_change()
        for l in range(1, n_lags+1):
            df[f"close_pct_lag{l}"] = df["close_pct"].shift(l)
    # price lags if needed
    for f in base_features:
        if any(name.startswith(f"{f}_lag") for name in feature_names):
            for l in range(1, n_lags+1):
                df[f"{f}_lag{l}"] = df[f].shift(l)
    df_lags = df.dropna().reset_index(drop=True)
    if df_lags.empty:
        raise ValueError("No hay suficientes filas para generar lags. Aumentá 'Usar últimos N registros'.")
    Xi = df_lags.iloc[[-1]].copy()
    if use_feedback:
        if "prev_pred" in feature_names:
            Xi["prev_pred"] = st.session_state.get("prev_pred_streamlit", 0.0)
        if "prev_err" in feature_names:
            prev_pred = st.session_state.get("prev_pred_streamlit", 0.0)
            prev_real = st.session_state.get("prev_real_streamlit", 0.0)
            Xi["prev_err"] = prev_pred - prev_real
    for col in feature_names:
        if col not in Xi.columns:
            Xi[col] = 0.0
    Xi = Xi[feature_names]
    return Xi, df

def load_df(uploaded):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("Usando datos de demo: data/sample_binance.csv")
        df = pd.read_csv("data/sample_binance.csv")
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

def next_prediction(df, artifact, last_real_input):
    model = artifact["model"]
    BASE_FEATURES = artifact.get("base_features", ["close","volume","high","low","open"])
    N_LAGS = int(artifact.get("n_lags", 5))
    USE_FEEDBACK = bool(artifact.get("use_feedback", True))
    feature_names = artifact.get("feature_names", None)
    if feature_names is None and hasattr(model, "feature_names_in_"):
        feature_names = list(model.feature_names_in_)
    if feature_names is None:
        feature_names = [f"close_pct_lag{i}" for i in range(1, N_LAGS+1)]
    Xi, df_proc = ensure_feature_names(df, feature_names, BASE_FEATURES, N_LAGS, USE_FEEDBACK)
    yhat = float(model.predict(Xi)[0])
    if USE_FEEDBACK and last_real_input and str(last_real_input).strip():
        try:
            real_pct = float(str(last_real_input).replace(",", "."))
            st.session_state["prev_real_streamlit"] = real_pct/100.0
            st.session_state["prev_pred_streamlit"] = yhat
        except:
            st.warning("No pude interpretar el retorno real ingresado (usa 0.8 ó -1.2).")
    return yhat, df_proc, feature_names

st.title("Predicción de % de cambio (siguiente período) — DecisionTreeRegressor con feedback")
artifact = load_artifact()

with st.sidebar:
    st.header("Datos de entrada")
    up = st.file_uploader("Subí CSV (open_time, open, high, low, close, volume, ...)", type=["csv"])
    n_recent = st.number_input("Usar últimos N registros", 200, 20000, 400, step=50)
    st.divider()
    st.header("Feedback (opcional)")
    last_real = st.text_input("Retorno real del último día (en %, ej: 0.8 o -1.2).")
    btn_predict = st.button("Predecir siguiente período")

df = load_df(up)

tab1, tab2 = st.tabs(["Exploración", "Predicción"])

with tab1:
    st.subheader("Exploración rápida")
    st.dataframe(df.tail(10))
    chart = alt.Chart(df.tail(200)).mark_line().encode(x="date:T", y=alt.Y("close:Q", title="Close")).properties(height=280)
    st.altair_chart(chart, use_container_width=True)

with tab2:
    if btn_predict:
        try:
            df_recent = df.tail(int(n_recent)).copy()
            yhat, df_proc, feat_names = next_prediction(df_recent, artifact, last_real)
            st.success(f"Predicción retorno próximo período: **{yhat*100:.3f}%**")
            ctx = df_proc.tail(60)[["date","close"]].copy()
            ctx["predicted_next_close"] = np.nan
            ctx.iloc[-1, ctx.columns.get_loc("predicted_next_close")] = ctx["close"].iloc[-1]*(1.0 + yhat)
            base = alt.Chart(ctx).encode(x="date:T").properties(height=280)
            real_line = base.mark_line().encode(y=alt.Y("close:Q", title="Close"))
            pred_point = base.mark_point(size=80).encode(y="predicted_next_close:Q", tooltip=["date:T","predicted_next_close:Q"])
            st.altair_chart(alt.layer(real_line, pred_point), use_container_width=True)
            with st.expander("Detalles técnicos"):
                st.write("Features usadas por el modelo (orden exacto):")
                st.code(feat_names)
        except Exception as e:
            st.error(f"No pude predecir: {e}")
    else:
        st.info("Cargá un CSV o usá el demo y presioná *Predecir*.")
