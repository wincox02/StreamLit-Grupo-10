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
    art = joblib.load(path)
    # HARD REQUIREMENT: deben existir feature_names
    feat = art.get("feature_names", None)
    if feat is None and hasattr(art["model"], "feature_names_in_"):
        feat = list(art["model"].feature_names_in_)
        art["feature_names"] = feat  # normalizamos dentro del artefacto en memoria
    if art.get("feature_names", None) is None:
        st.error("El artefacto no trae 'feature_names' y el modelo no expone 'feature_names_in_'. "
                 "No puedo garantizar coherencia de features. Volvé a exportar el modelo con feature_names.")
        st.stop()
    return art

artifact = load_artifact()
model = artifact["model"]
FEATURE_NAMES = artifact["feature_names"]      # <- usaremos SIEMPRE estas
BASE_FEATURES = artifact.get("base_features", ["close","volume","high","low","open"])
N_LAGS = int(artifact.get("n_lags", 5))
USE_FEEDBACK = bool(artifact.get("use_feedback", True))
SCALER_Y = artifact.get("scaler_y", None)     # opcional

# DEBUG: Mostrar info del modelo al cargar
st.sidebar.info(f"**Modelo cargado:**\n- Features: {len(FEATURE_NAMES)}\n- Lags: {N_LAGS}\n- Feedback: {USE_FEEDBACK}")
with st.sidebar.expander("🔍 Ver features del modelo"):
    st.write("**Features esperadas por el modelo:**")
    for i, feat in enumerate(FEATURE_NAMES, 1):
        st.text(f"{i}. {feat}")

# ---------- Utilidades ----------
@st.cache_data
def load_df(uploaded_file):
    """Carga el CSV desde el uploader o usa uno por defecto."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Usar un CSV por defecto si existe
        try:
            df = pd.read_csv("BTCUSDT_1d_last_year.csv")
        except:
            st.error("No se subió archivo y no existe CSV por defecto. Subí un archivo CSV.")
            st.stop()
    
    # Asegurar columna de fecha
    if "date" not in df.columns and "open_time" in df.columns:
        df["date"] = pd.to_datetime(df["open_time"], unit="ms")
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    
    return df

def ensure_feature_names(df_raw, feature_names, base_features, n_lags, use_feedback=True):
    """
    Construye EXACTAMENTE las columnas 'feature_names' que el modelo vio en fit.
    IMPORTANTE: Replicar el preprocesamiento exacto del entrenamiento (3_v3.py)
    """
    df = df_raw.copy()

    # PASO 1: Calcular todos los _pct necesarios (multiplicar por 100 como en el entrenamiento!)
    for col_base in ["open", "high", "low", "close"]:
        col_pct = f"{col_base}_pct"
        if col_pct in feature_names or any(name.startswith(col_pct) for name in feature_names):
            if col_base in df.columns:
                df[col_pct] = df[col_base].pct_change() * 100.0  # ← MULTIPLICAR POR 100!
    
    # Volumen (puede ser "volume" o "volumen")
    for vol_name in ["volume", "volumen"]:
        col_pct = f"{vol_name}_pct"
        if col_pct in feature_names:
            if vol_name in df.columns:
                df[col_pct] = df[vol_name].pct_change() * 100.0

    # PASO 2: Medias móviles sobre close_pct (no sobre close!)
    if "ma3" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["ma3"] = df["close_pct"].rolling(window=3).mean()
    
    if "ma7" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["ma7"] = df["close_pct"].rolling(window=7).mean()
    
    # PASO 3: Volatilidad sobre close_pct
    if "volatilidad_7" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["volatilidad_7"] = df["close_pct"].rolling(window=7).std()

    # PASO 4: Lags de close_pct
    if any(name.startswith("close_pct_lag") for name in feature_names):
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        for l in range(1, n_lags + 1):
            col = f"close_pct_lag{l}"
            if col in feature_names:
                df[col] = df["close_pct"].shift(l)

    # Lags de features base solo si aparecen en feature_names
    for f in base_features:
        if any(name.startswith(f"{f}_lag") for name in feature_names):
            if f not in df.columns:
                raise KeyError(f"Falta la columna '{f}' en el dataset de entrada.")
            for l in range(1, n_lags + 1):
                col = f"{f}_lag{l}"
                if col in feature_names:
                    df[col] = df[f].shift(l)

    # Última fila con lags completos
    df_lags = df.dropna().reset_index(drop=True)
    if df_lags.empty:
        raise ValueError("No hay suficientes filas para generar lags. Aumentá 'Usar últimos N registros' o quitá el manual si no alcanza.")

    Xi = df_lags.iloc[[-1]].copy()

    # Feedback
    if use_feedback:
        if "prev_pred" in feature_names:
            Xi.loc[:, "prev_pred"] = st.session_state.get("prev_pred_streamlit", 0.0)
        if "prev_err" in feature_names:
            prev_pred = st.session_state.get("prev_pred_streamlit", 0.0)
            prev_real = st.session_state.get("prev_real_streamlit", 0.0)
            Xi.loc[:, "prev_err"] = prev_pred - prev_real

    # Asegurar mismas columnas y orden exacto
    for col in feature_names:
        if col not in Xi.columns:
            Xi.loc[:, col] = 0.0
    Xi = Xi.loc[:, list(dict.fromkeys(feature_names))]  # quita duplicados si los hubiese

    return Xi, df_lags

def next_prediction(df_recent, last_real_input, debug_placeholder=None):
    # Usar SIEMPRE las features reales del fit:
    feature_names = FEATURE_NAMES

    Xi, df_proc = ensure_feature_names(
        df_raw=df_recent,
        feature_names=feature_names,
        base_features=BASE_FEATURES,
        n_lags=N_LAGS,
        use_feedback=USE_FEEDBACK
    )

    # DEBUG: Mostrar datos antes de la predicción en un expander
    if debug_placeholder:
        with debug_placeholder.container():
            with st.expander("� VER DATOS ENVIADOS AL MODELO (Debug)", expanded=True):
                st.write(f"**Shape:** {Xi.shape[0]} fila(s) × {Xi.shape[1]} columna(s)")
                
                # Estadísticas generales
                zeros_count = (Xi.values == 0).sum()
                total_values = Xi.size
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Valores en 0", f"{zeros_count}/{total_values}")
                col2.metric("Mínimo", f"{Xi.values.min():.6f}")
                col3.metric("Máximo", f"{Xi.values.max():.6f}")
                col4.metric("Promedio", f"{Xi.values.mean():.6f}")
                
                # Mostrar TODOS los valores en un dataframe transpuesto
                st.write("**Todos los valores enviados al modelo:**")
                Xi_display = Xi.T.copy()
                Xi_display.columns = ['Valor']
                st.dataframe(Xi_display, height=400)
                
                # También en formato de texto para copiar/pegar
                st.write("**Valores en formato texto:**")
                valores_texto = ""
                for col in Xi.columns:
                    valores_texto += f"{col}: {Xi[col].values[0]:.8f}\n"
                st.text_area("Copiar valores", valores_texto, height=200)

    # Predicción (respetando un posible scaler_y del target)
    yhat_scaled = float(model.predict(Xi)[0])
    
    # El modelo predice en escala del StandardScaler, hay que desescalar
    if SCALER_Y is not None:
        yhat = float(SCALER_Y.inverse_transform(np.array([[yhat_scaled]])).ravel()[0])
    else:
        yhat = yhat_scaled
    
    # yhat ahora está en escala de % (ya multiplicado por 100 en el preprocesamiento)

    # Actualizar feedback si nos dieron el real del último día (en %)
    if USE_FEEDBACK and last_real_input and str(last_real_input).strip():
        try:
            real_pct = float(str(last_real_input).replace(",", "."))
            # real_pct ya está en escala %, igual que yhat
            st.session_state["prev_real_streamlit"] = real_pct
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

            # Crear placeholder para mostrar debug antes de predecir
            debug_placeholder = st.empty()
            
            # Predecir
            yhat, df_proc, feat_names = next_prediction(df_recent, last_real, debug_placeholder)
            # yhat ya está en escala de % (el modelo predice directamente en %)
            st.success(f"Predicción retorno próximo período: **{yhat:.3f}%**")

            # Contexto visual: último tramo + punto de cierre predicho
            ctx = df_proc.tail(60)[["date","close"]].copy()
            ctx["predicted_next_close"] = np.nan
            # yhat está en %, hay que dividir por 100 para usarlo como factor
            ctx.iloc[-1, ctx.columns.get_loc("predicted_next_close")] = ctx["close"].iloc[-1]*(1.0 + yhat/100.0)

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
