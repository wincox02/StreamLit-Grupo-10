# main.py / app.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import joblib

st.set_page_config(page_title="Predicción % cambio — DTR con feedback", layout="wide")
st.title("Predicción de % de cambio (siguiente período) — DecisionTreeRegressor con feedback")

# ---------- Carga del artefacto ----------
@st.cache_resource
def load_artifact(path="models/model_feedback.pkl"):
    return joblib.load(path)

artifact = load_artifact()
model = artifact["model"]
BASE_FEATURES = artifact.get("base_features", ["close","volume","high","low","open"])
N_LAGS = int(artifact.get("n_lags", 5))
USE_FEEDBACK = bool(artifact.get("use_feedback", True))

# ---------- Utilidades ----------
def load_df(uploaded):
    """Carga CSV (o demo) y normaliza fecha."""
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("Usando muestra de datos demo (data/sample_binance.csv).")
        df = pd.read_csv("data/sample_binance.csv")

    # Normalizar fecha
    if "open_time" in df.columns:
        # Si viene en ms (int)
        if np.issubdtype(type(df["open_time"].iloc[0]), np.integer):
            df["date"] = pd.to_datetime(df["open_time"], unit="ms")
        else:
            df["date"] = pd.to_datetime(df["open_time"])
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        raise ValueError("No encuentro 'open_time' o 'date' en el CSV.")

    return df.sort_values("date").reset_index(drop=True)

def ensure_feature_names(df_raw, feature_names, base_features, n_lags, use_feedback=True):
    """
    Construye EXACTAMENTE las columnas 'feature_names' que el modelo vio en fit.
    - Si el modelo usó close_pct y sus lags, las crea.
    - Si usó lags de precio (close_lagN, open_lagN, etc.), también.
    - Añade prev_pred/prev_err si el modelo los espera (feedback).
    """
    df = df_raw.copy()

    # 1) Derivados de retornos si el modelo los usa
    if any(name.startswith("close_pct") for name in feature_names):
        df["close_pct"] = df["close"].pct_change()
        for l in range(1, n_lags + 1):
            df[f"close_pct_lag{l}"] = df["close_pct"].shift(l)

    # 2) Lags de features base si el modelo los usa
    for f in base_features:
        if any(name.startswith(f"{f}_lag") for name in feature_names):
            for l in range(1, n_lags + 1):
                if f not in df.columns:
                    raise KeyError(f"Falta la columna '{f}' en el dataset de entrada.")
                df[f"{f}_lag{l}"] = df[f].shift(l)

    # 3) Última fila con lags completos
    df_lags = df.dropna().reset_index(drop=True)
    if df_lags.empty:
        raise ValueError("No hay suficientes filas para generar lags. Aumentá 'Usar últimos N registros'.")
    Xi = df_lags.iloc[[-1]].copy()

    # 4) Feedback
    if use_feedback:
        if "prev_pred" in feature_names:
            Xi.loc[:, "prev_pred"] = st.session_state.get("prev_pred_streamlit", 0.0)
        if "prev_err" in feature_names:
            prev_pred = st.session_state.get("prev_pred_streamlit", 0.0)
            prev_real = st.session_state.get("prev_real_streamlit", 0.0)
            Xi.loc[:, "prev_err"] = prev_pred - prev_real

    # 5) Asegurar mismas columnas y orden EXACTO (fix de "Columns must be same length as key")
    for col in feature_names:
        if col not in Xi.columns:
            Xi.loc[:, col] = 0.0  # fallback seguro para columnas ausentes
    # quita duplicados conservando orden si los hubiera
    feature_names_unique = list(dict.fromkeys(feature_names))
    Xi = Xi.loc[:, feature_names_unique]

    return Xi, df

def next_prediction(df_recent, last_real_input):
    """Arma Xi con las mismas features del fit y predice el próximo retorno."""
    # Detectar lista exacta de features vistas en fit
    feature_names = artifact.get("feature_names", None)
    if feature_names is None and hasattr(model, "feature_names_in_"):
        feature_names = list(model.feature_names_in_)
    if feature_names is None:
        # Último recurso: asumir retornos con lags
        feature_names = [f"close_pct_lag{i}" for i in range(1, N_LAGS + 1)]

    Xi, df_proc = ensure_feature_names(
        df_raw=df_recent,
        feature_names=feature_names,
        base_features=BASE_FEATURES,
        n_lags=N_LAGS,
        use_feedback=USE_FEEDBACK
    )

    # Predicción
    yhat = float(model.predict(Xi)[0])

    # Actualizar feedback si nos dieron el real del último día (en %)
    if USE_FEEDBACK and last_real_input and str(last_real_input).strip():
        try:
            real_pct = float(str(last_real_input).replace(",", "."))
            st.session_state["prev_real_streamlit"] = real_pct / 100.0
            st.session_state["prev_pred_streamlit"] = yhat
        except:
            st.warning("No pude interpretar el retorno real ingresado (usa 0.8 ó -1.2).")

    return yhat, df_proc, feature_names

# ---------- UI ----------
with st.sidebar:
    st.header("Datos de entrada")
    up = st.file_uploader("Subí CSV con columnas Binance (open_time, open, high, low, close, volume, ...)", type=["csv"])
    n_recent = st.number_input("Usar últimos N registros", 200, 20000, 400, step=50)
    st.caption("Necesitamos al menos N_LAGS+1 filas para generar la próxima predicción.")

    st.divider()
    st.header("Feedback opcional (último día real)")
    last_real = st.text_input("Retorno real del último día (en %, ej: 0.8 o -1.2).")

df = load_df(up)

tab1, tab2 = st.tabs(["Exploración", "Predicción"])

with tab1:
    st.subheader("Exploración rápida")
    st.dataframe(df.tail(10))
    chart = alt.Chart(df.tail(200)).mark_line().encode(
        x="date:T", y=alt.Y("close:Q", title="Close")
    ).properties(height=280)
    st.altair_chart(chart, use_container_width=True)

with tab2:
    st.subheader("Predicción del siguiente período")

    # --- Ingreso manual de OHLCV del "último día" ---
    with st.expander("Ingresar manualmente el último día (OHLCV)"):
        c1, c2, c3, c4, c5 = st.columns(5)
        m_open  = c1.number_input("Open",   value=float(df["open"].iloc[-1]),  format="%.6f")
        m_high  = c2.number_input("High",   value=float(df["high"].iloc[-1]),  format="%.6f")
        m_low   = c3.number_input("Low",    value=float(df["low"].iloc[-1]),   format="%.6f")
        m_close = c4.number_input("Close",  value=float(df["close"].iloc[-1]), format="%.6f")
        m_vol   = c5.number_input("Volume", value=float(df["volume"].iloc[-1]),format="%.6f")
        use_manual = st.checkbox("Usar estos valores como último día", value=False)

    if st.button("Predecir siguiente período"):
        try:
            # Tomar últimos N
            df_recent = df.tail(int(n_recent)).copy()

            # Si se eligió ingresar manual, anexar ese día como el más reciente
            if use_manual:
                next_date = df_recent["date"].iloc[-1] + pd.Timedelta(days=1)
                last = {
                    "symbol":   df_recent["symbol"].iloc[-1]   if "symbol"   in df_recent.columns else "ASSET",
                    "interval": df_recent["interval"].iloc[-1] if "interval" in df_recent.columns else "1d",
                    "open_time": int(next_date.value/1e6),
                    "open": m_open, "high": m_high, "low": m_low, "close": m_close, "volume": m_vol,
                    "date": next_date,
                }
                df_recent = pd.concat([df_recent, pd.DataFrame([last])], ignore_index=True)

            # Predecir
            yhat, df_proc, feat_names = next_prediction(df_recent, last_real)
            st.success(f"Predicción retorno próximo período: **{yhat*100:.3f}%**")

            # Contexto visual: último tramo + punto de cierre predicho
            ctx = df_proc.tail(60)[["date","close"]].copy()
            ctx["predicted_next_close"] = np.nan
            ctx.iloc[-1, ctx.columns.get_loc("predicted_next_close")] = ctx["close"].iloc[-1]*(1.0 + yhat)

            base = alt.Chart(ctx).encode(x="date:T").properties(height=300)
            real_line = base.mark_line().encode(y=alt.Y("close:Q", title="Close"))
            pred_point = base.mark_point(size=80).encode(
                y="predicted_next_close:Q",
                tooltip=["date:T","predicted_next_close:Q"]
            )
            st.altair_chart(alt.layer(real_line, pred_point), use_container_width=True)

            with st.expander("Detalles técnicos"):
                st.write("Features usadas por el modelo (orden exacto):")
                st.code(feat_names)

        except Exception as e:
            st.error(f"No pude predecir: {e}")
