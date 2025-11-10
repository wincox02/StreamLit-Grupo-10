# main_mejorado.py - Aplicación completa de predicción de Bitcoin
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from datetime import timedelta

st.set_page_config(
    page_title="Bitcoin Predictor - Análisis y Predicción",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #f7931a;
        margin-bottom: 2rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 3rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES DE CARGA Y PROCESAMIENTO ====================

@st.cache_resource
def load_artifact(path="models/model_feedback.pkl"):
    """Carga el modelo pre-entrenado"""
    try:
        art = joblib.load(path)
        feat = art.get("feature_names", None)
        if feat is None and hasattr(art["model"], "feature_names_in_"):
            feat = list(art["model"].feature_names_in_)
            art["feature_names"] = feat
        if art.get("feature_names", None) is None:
            st.error("El artefacto no contiene 'feature_names'. Por favor, vuelve a exportar el modelo.")
            st.stop()
        return art
    except FileNotFoundError:
        st.error(f"No se encontró el modelo en {path}. Por favor, asegúrate de tener el archivo del modelo.")
        st.stop()

@st.cache_data
def load_df(uploaded_file=None):
    """Carga el CSV desde el uploader o usa uno por defecto"""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        try:
            df = pd.read_csv("BTCUSDT_1d_last_year.csv")
        except:
            st.error("No se encontró archivo CSV por defecto. Por favor, sube un archivo CSV.")
            st.stop()
    
    # Asegurar columna de fecha
    if "date" not in df.columns and "open_time" in df.columns:
        df["date"] = pd.to_datetime(df["open_time"], unit="ms")
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    
    df = df.sort_values("date").reset_index(drop=True)
    return df

def ensure_feature_names(df_raw, feature_names, base_features, n_lags, use_feedback=True):
    """Construye las features exactas que el modelo necesita"""
    df = df_raw.copy()
    
    # PASO 1: Calcular porcentajes de cambio (multiplicar por 100)
    for col_base in ["open", "high", "low", "close"]:
        col_pct = f"{col_base}_pct"
        if col_pct in feature_names or any(name.startswith(col_pct) for name in feature_names):
            if col_base in df.columns:
                df[col_pct] = df[col_base].pct_change() * 100.0
    
    # Volumen
    for vol_name in ["volume", "volumen"]:
        col_pct = f"{vol_name}_pct"
        if col_pct in feature_names:
            if vol_name in df.columns:
                df[col_pct] = df[vol_name].pct_change() * 100.0

    # PASO 2: Medias móviles
    if "ma3" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["ma3"] = df["close_pct"].rolling(window=3).mean()
    
    if "ma7" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["ma7"] = df["close_pct"].rolling(window=7).mean()
    
    # PASO 3: Volatilidad
    if "volatilidad_7" in feature_names:
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        df["volatilidad_7"] = df["close_pct"].rolling(window=7).std()

    # PASO 4: Lags
    if any(name.startswith("close_pct_lag") for name in feature_names):
        if "close_pct" not in df.columns:
            df["close_pct"] = df["close"].pct_change() * 100.0
        for l in range(1, n_lags + 1):
            col = f"close_pct_lag{l}"
            if col in feature_names:
                df[col] = df["close_pct"].shift(l)

    # Lags de features base
    for f in base_features:
        if any(name.startswith(f"{f}_lag") for name in feature_names):
            if f not in df.columns:
                raise KeyError(f"Falta la columna '{f}' en el dataset de entrada.")
            for l in range(1, n_lags + 1):
                col = f"{f}_lag{l}"
                if col in feature_names:
                    df[col] = df[f].shift(l)

    # Eliminar NaNs solo en las columnas de features
    df_lags = df.dropna(subset=feature_names).reset_index(drop=True)
    if df_lags.empty:
        raise ValueError("No hay suficientes filas para generar lags.")
    
    Xi = df_lags.iloc[[-1]].copy()

    # Feedback
    if use_feedback:
        if "prev_pred" in feature_names:
            Xi.loc[:, "prev_pred"] = st.session_state.get("prev_pred_streamlit", 0.0)
        if "prev_err" in feature_names:
            prev_pred = st.session_state.get("prev_pred_streamlit", 0.0)
            prev_real = st.session_state.get("prev_real_streamlit", 0.0)
            Xi.loc[:, "prev_err"] = prev_pred - prev_real

    # Asegurar columnas en el orden correcto
    for col in feature_names:
        if col not in Xi.columns:
            Xi.loc[:, col] = 0.0
    Xi = Xi.loc[:, list(dict.fromkeys(feature_names))]

    return Xi, df_lags

def predict_next_day(df_recent, model, feature_names, base_features, n_lags, use_feedback, scaler_y=None):
    """Realiza una predicción para el próximo día"""
    Xi, df_proc = ensure_feature_names(
        df_raw=df_recent,
        feature_names=feature_names,
        base_features=base_features,
        n_lags=n_lags,
        use_feedback=use_feedback
    )
    
    yhat_scaled = float(model.predict(Xi)[0])
    
    if scaler_y is not None:
        yhat = float(scaler_y.inverse_transform(np.array([[yhat_scaled]])).ravel()[0])
    else:
        yhat = yhat_scaled
    
    return yhat, df_proc, Xi

def predict_multiple_days(df_recent, model, feature_names, base_features, n_lags, use_feedback, scaler_y, n_days=7):
    """Realiza predicciones para múltiples días con retroalimentación"""
    predictions = []
    df_working = df_recent.copy()
    
    for day in range(n_days):
        # Predecir próximo día
        yhat, df_proc, Xi = predict_next_day(
            df_working, model, feature_names, base_features, n_lags, use_feedback, scaler_y
        )
        
        # Obtener último precio de cierre
        last_close = df_working["close"].iloc[-1]
        next_close = last_close * (1.0 + yhat / 100.0)
        next_date = df_working["date"].iloc[-1] + timedelta(days=1)
        
        predictions.append({
            "date": next_date,
            "predicted_change_pct": yhat,
            "predicted_close": next_close,
            "day_number": day + 1
        })
        
        # Crear nueva fila con la predicción para retroalimentación
        new_row = {
            "date": next_date,
            "open": next_close,
            "high": next_close * 1.01,  # Aproximación
            "low": next_close * 0.99,   # Aproximación
            "close": next_close,
            "volume": df_working["volume"].iloc[-1]
        }
        
        # Agregar columnas adicionales si existen
        if "symbol" in df_working.columns:
            new_row["symbol"] = df_working["symbol"].iloc[-1]
        if "interval" in df_working.columns:
            new_row["interval"] = df_working["interval"].iloc[-1]
        if "open_time" in df_working.columns:
            new_row["open_time"] = int(next_date.timestamp() * 1000)
        
        df_working = pd.concat([df_working, pd.DataFrame([new_row])], ignore_index=True)
    
    return pd.DataFrame(predictions), df_working

# ==================== FUNCIONES DE VISUALIZACIÓN ====================

def create_candlestick_chart(df, title="Análisis de Precios Bitcoin", show_predictions=None):
    """Crea un gráfico de velas interactivo con zoom"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(title, 'Volumen')
    )
    
    # Gráfico de velas
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='OHLC',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    # Añadir medias móviles si existen suficientes datos
    if len(df) >= 7:
        ma7 = df['close'].rolling(window=7).mean()
        fig.add_trace(
            go.Scatter(x=df['date'], y=ma7, name='MA7', line=dict(color='orange', width=1)),
            row=1, col=1
        )
    
    if len(df) >= 30:
        ma30 = df['close'].rolling(window=30).mean()
        fig.add_trace(
            go.Scatter(x=df['date'], y=ma30, name='MA30', line=dict(color='blue', width=1)),
            row=1, col=1
        )
    
    # Añadir predicciones si se proporcionan
    if show_predictions is not None and not show_predictions.empty:
        fig.add_trace(
            go.Scatter(
                x=show_predictions['date'],
                y=show_predictions['predicted_close'],
                mode='lines+markers',
                name='Predicción',
                line=dict(color='red', width=3, dash='dash'),
                marker=dict(size=8, symbol='star')
            ),
            row=1, col=1
        )
    
    # Volumen
    colors = ['red' if row['open'] > row['close'] else 'green' for idx, row in df.iterrows()]
    fig.add_trace(
        go.Bar(x=df['date'], y=df['volume'], name='Volumen', marker_color=colors),
        row=2, col=1
    )
    
    # Configurar layout
    fig.update_layout(
        height=700,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Configurar ejes
    fig.update_xaxes(title_text="Fecha", row=2, col=1)
    fig.update_yaxes(title_text="Precio (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volumen", row=2, col=1)
    
    return fig

def create_price_comparison_chart(df, predictions_1d, predictions_5d, predictions_10d):
    """Crea un gráfico comparativo de predicciones a diferentes plazos"""
    fig = go.Figure()
    
    # Línea real
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['close'],
        mode='lines',
        name='Precio Real',
        line=dict(color='black', width=2)
    ))
    
    # Predicción 1 día
    if predictions_1d is not None and not predictions_1d.empty:
        fig.add_trace(go.Scatter(
            x=predictions_1d['date'],
            y=predictions_1d['predicted_close'],
            mode='lines+markers',
            name='Predicción 1 día',
            line=dict(color='green', width=2, dash='dash')
        ))
    
    # Predicción 5 días
    if predictions_5d is not None and not predictions_5d.empty:
        fig.add_trace(go.Scatter(
            x=predictions_5d['date'],
            y=predictions_5d['predicted_close'],
            mode='lines+markers',
            name='Predicción 5 días',
            line=dict(color='orange', width=2, dash='dot')
        ))
    
    # Predicción 10 días
    if predictions_10d is not None and not predictions_10d.empty:
        fig.add_trace(go.Scatter(
            x=predictions_10d['date'],
            y=predictions_10d['predicted_close'],
            mode='lines+markers',
            name='Predicción 10 días',
            line=dict(color='red', width=2, dash='dashdot')
        ))
    
    fig.update_layout(
        title="Comparación de Predicciones a Diferentes Plazos",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
        height=600,
        hovermode='x unified',
        template='plotly_white',
        showlegend=True
    )
    
    return fig

# ==================== INICIALIZACIÓN ====================

# Cargar modelo y datos
artifact = load_artifact()
model = artifact["model"]
FEATURE_NAMES = artifact["feature_names"]
BASE_FEATURES = artifact.get("base_features", ["close","volume","high","low","open"])
N_LAGS = int(artifact.get("n_lags", 5))
USE_FEEDBACK = bool(artifact.get("use_feedback", True))
SCALER_Y = artifact.get("scaler_y", None)

# Cargar datos
df = load_df()

# Inicializar session state
if 'predictions_1d' not in st.session_state:
    st.session_state.predictions_1d = None
if 'predictions_5d' not in st.session_state:
    st.session_state.predictions_5d = None
if 'predictions_10d' not in st.session_state:
    st.session_state.predictions_10d = None
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False

# ==================== INTERFAZ DE USUARIO ====================

# Crear tabs
tab_inicio, tab_prediccion, tab_exploracion, tab_modelo = st.tabs([
    "🏠 Inicio",
    "📈 Predicción",
    "🔍 Exploración de Datos",
    "🧠 Sobre el Modelo"
])

# ==================== TAB INICIO ====================
with tab_inicio:
    st.markdown('<h1 class="main-title">₿ Bitcoin Price Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistema de Predicción Basado en Machine Learning</p>', unsafe_allow_html=True)
    
    # Descripción general
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>🎯 ¿Qué hace esta aplicación?</h3>
        <p>Este sistema utiliza un modelo de <b>Decision Tree Regressor</b> entrenado con datos históricos 
        de Bitcoin para predecir el cambio porcentual del precio en el próximo período.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📊 Características Principales
        
        1. **Predicción de Mañana**: Predice el cambio de precio para el siguiente día
        2. **Predicción Múltiple**: Predice varios días hacia adelante con retroalimentación
        3. **Gráficos Interactivos**: Visualización tipo trading con zoom y filtros
        4. **Análisis Comparativo**: Compara predicciones a 1, 5 y 10 días
        
        ### 🔧 ¿Cómo Funciona el Modelo?
        
        El modelo analiza múltiples features para hacer sus predicciones:
        
        - **Precios OHLC**: Open, High, Low, Close y sus cambios porcentuales
        - **Volumen**: Cambios en el volumen de trading
        - **Lags Temporales**: Valores históricos de períodos anteriores
        - **Medias Móviles**: MA3 y MA7 para identificar tendencias
        - **Volatilidad**: Desviación estándar de los últimos 7 períodos
        - **Retroalimentación**: Aprende de predicciones anteriores (opcional)
        """)
        
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ Advertencia Importante</h4>
        <p>Este modelo es solo para fines educativos y de investigación. 
        <b>NO</b> debe utilizarse como única base para decisiones de inversión.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas del modelo
        st.markdown("### 📊 Información del Modelo")
        st.metric("Features Utilizadas", len(FEATURE_NAMES))
        st.metric("Lags Temporales", N_LAGS)
        st.metric("Retroalimentación", "Activada" if USE_FEEDBACK else "Desactivada")
        
    # Guía de uso
    st.markdown("---")
    st.markdown("### 🚀 Cómo Usar la Aplicación")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Explorar Datos
        Ve a la pestaña **Exploración de Datos** para:
        - Ver datos históricos
        - Analizar gráficos interactivos
        - Aplicar filtros temporales
        """)
        
    with col2:
        st.markdown("""
        #### 2️⃣ Hacer Predicciones
        Ve a la pestaña **Predicción** para:
        - Predecir el próximo día
        - Predecir múltiples días
        - Ver comparaciones
        """)
        
    with col3:
        st.markdown("""
        #### 3️⃣ Entender el Modelo
        Ve a la pestaña **Sobre el Modelo** para:
        - Ver métricas de rendimiento
        - Entender las features
        - Análisis técnico
        """)

# ==================== TAB PREDICCIÓN ====================
with tab_prediccion:
    st.header("📈 Predicción de Precios")
    
    # Opciones de predicción
    pred_col1, pred_col2 = st.columns(2)
    
    with pred_col1:
        st.subheader("🔮 Predicción de Mañana")
        st.markdown("""
        Predice el cambio de precio para el próximo día basándose en los datos más recientes.
        """)
        
        # Opciones de configuración
        with st.expander("⚙️ Configuración Avanzada"):
            n_recent_simple = st.slider("Últimos N registros para predecir", 100, 1000, 400, 50)
            show_features_simple = st.checkbox("Mostrar features enviadas al modelo", value=False)
        
        if st.button("🎯 Predecir Mañana", type="primary", use_container_width=True):
            with st.spinner("Calculando predicción..."):
                try:
                    df_recent = df.tail(n_recent_simple).copy()
                    yhat, df_proc, Xi = predict_next_day(
                        df_recent, model, FEATURE_NAMES, BASE_FEATURES, N_LAGS, USE_FEEDBACK, SCALER_Y
                    )
                    
                    last_close = df_proc["close"].iloc[-1]
                    predicted_close = last_close * (1.0 + yhat / 100.0)
                    
                    # Mostrar resultados
                    st.success("✅ Predicción Completada")
                    
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    metric_col1.metric("Cambio Predicho", f"{yhat:.3f}%", 
                                     delta=f"{yhat:.3f}%", 
                                     delta_color="normal")
                    metric_col2.metric("Precio Actual", f"${last_close:,.2f}")
                    metric_col3.metric("Precio Predicho", f"${predicted_close:,.2f}",
                                     delta=f"${predicted_close - last_close:,.2f}")
                    
                    # Mostrar features si se solicita
                    if show_features_simple:
                        with st.expander("📊 Features Enviadas al Modelo"):
                            st.dataframe(Xi.T, use_container_width=True)
                    
                    # Crear predicción para visualización
                    next_date = df_proc["date"].iloc[-1] + timedelta(days=1)
                    pred_df = pd.DataFrame([{
                        "date": next_date,
                        "predicted_close": predicted_close,
                        "predicted_change_pct": yhat
                    }])
                    
                    st.session_state.predictions_1d = pred_df
                    
                    # Gráfico
                    fig = create_candlestick_chart(
                        df_proc.tail(60),
                        "Predicción para Mañana",
                        pred_df
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error en la predicción: {e}")
    
    with pred_col2:
        st.subheader("📅 Predicción Múltiples Días")
        st.markdown("""
        Predice varios días hacia adelante usando retroalimentación de predicciones anteriores.
        """)
        
        # Opciones de configuración
        with st.expander("⚙️ Configuración Avanzada"):
            n_recent_multi = st.slider("Últimos N registros base", 100, 1000, 400, 50, key="multi")
            n_days_predict = st.slider("Días a predecir", 1, 30, 7, 1)
            show_features_multi = st.checkbox("Mostrar detalles de predicción", value=False, key="multi_feat")
        
        if st.button("📊 Predecir Múltiples Días", type="primary", use_container_width=True):
            with st.spinner(f"Calculando predicciones para {n_days_predict} días..."):
                try:
                    df_recent = df.tail(n_recent_multi).copy()
                    predictions_df, df_extended = predict_multiple_days(
                        df_recent, model, FEATURE_NAMES, BASE_FEATURES, 
                        N_LAGS, USE_FEEDBACK, SCALER_Y, n_days_predict
                    )
                    
                    st.success(f"✅ Predicción de {n_days_predict} días completada")
                    
                    # Mostrar tabla de predicciones
                    st.dataframe(
                        predictions_df[["day_number", "date", "predicted_change_pct", "predicted_close"]]
                        .style.format({
                            "predicted_change_pct": "{:.3f}%",
                            "predicted_close": "${:,.2f}"
                        }),
                        use_container_width=True
                    )
                    
                    # Guardar predicciones según días
                    if n_days_predict == 1:
                        st.session_state.predictions_1d = predictions_df
                    elif n_days_predict == 5:
                        st.session_state.predictions_5d = predictions_df
                    elif n_days_predict == 10:
                        st.session_state.predictions_10d = predictions_df
                    
                    # Gráfico con todas las predicciones
                    fig = create_candlestick_chart(
                        df_extended.tail(60 + n_days_predict),
                        f"Predicción para {n_days_predict} Días",
                        predictions_df
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Estadísticas de la predicción
                    if show_features_multi:
                        with st.expander("📊 Estadísticas de Predicción"):
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Cambio Promedio", f"{predictions_df['predicted_change_pct'].mean():.3f}%")
                            col2.metric("Cambio Máximo", f"{predictions_df['predicted_change_pct'].max():.3f}%")
                            col3.metric("Cambio Mínimo", f"{predictions_df['predicted_change_pct'].min():.3f}%")
                            col4.metric("Desv. Estándar", f"{predictions_df['predicted_change_pct'].std():.3f}%")
                    
                except Exception as e:
                    st.error(f"❌ Error en la predicción múltiple: {e}")
    
    # Sección de comparación
    st.markdown("---")
    st.subheader("📊 Comparación de Predicciones")
    st.markdown("Compara predicciones a diferentes plazos para entender mejor las tendencias.")
    
    comp_col1, comp_col2 = st.columns([3, 1])
    
    with comp_col2:
        st.markdown("#### 🎮 Controles")
        if st.button("🔄 Generar Comparación Completa", use_container_width=True):
            with st.spinner("Generando predicciones comparativas..."):
                try:
                    df_recent = df.tail(400).copy()
                    
                    # Predicción 1 día
                    pred_1d, _, _ = predict_next_day(
                        df_recent, model, FEATURE_NAMES, BASE_FEATURES, N_LAGS, USE_FEEDBACK, SCALER_Y
                    )
                    last_close = df_recent["close"].iloc[-1]
                    next_date = df_recent["date"].iloc[-1] + timedelta(days=1)
                    st.session_state.predictions_1d = pd.DataFrame([{
                        "date": next_date,
                        "predicted_close": last_close * (1.0 + pred_1d / 100.0),
                        "predicted_change_pct": pred_1d
                    }])
                    
                    # Predicción 5 días
                    st.session_state.predictions_5d, _ = predict_multiple_days(
                        df_recent, model, FEATURE_NAMES, BASE_FEATURES, 
                        N_LAGS, USE_FEEDBACK, SCALER_Y, 5
                    )
                    
                    # Predicción 10 días
                    st.session_state.predictions_10d, _ = predict_multiple_days(
                        df_recent, model, FEATURE_NAMES, BASE_FEATURES, 
                        N_LAGS, USE_FEEDBACK, SCALER_Y, 10
                    )
                    
                    st.success("✅ Comparación generada correctamente")
                    
                except Exception as e:
                    st.error(f"❌ Error generando comparación: {e}")
        
        if st.button("🗑️ Limpiar Predicciones", use_container_width=True):
            st.session_state.predictions_1d = None
            st.session_state.predictions_5d = None
            st.session_state.predictions_10d = None
            st.success("✅ Predicciones limpiadas")
    
    with comp_col1:
        if (st.session_state.predictions_1d is not None or 
            st.session_state.predictions_5d is not None or 
            st.session_state.predictions_10d is not None):
            
            fig_comparison = create_price_comparison_chart(
                df.tail(60),
                st.session_state.predictions_1d,
                st.session_state.predictions_5d,
                st.session_state.predictions_10d
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
        else:
            st.info("👆 Haz clic en 'Generar Comparación Completa' para ver el gráfico comparativo")

# ==================== TAB EXPLORACIÓN ====================
with tab_exploracion:
    st.header("🔍 Exploración de Datos Históricos")
    
    # Filtros
    st.subheader("⚙️ Filtros y Opciones")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        filter_option = st.selectbox(
            "Período a visualizar",
            ["Última Semana", "Último Mes", "Últimos 3 Meses", "Últimos 6 Meses", "Último Año", "Todo"]
        )
    
    with filter_col2:
        show_ma = st.checkbox("Mostrar Medias Móviles", value=True)
        
    with filter_col3:
        show_volume = st.checkbox("Mostrar Volumen", value=True)
    
    # Aplicar filtros
    if filter_option == "Última Semana":
        df_filtered = df.tail(7)
    elif filter_option == "Último Mes":
        df_filtered = df.tail(30)
    elif filter_option == "Últimos 3 Meses":
        df_filtered = df.tail(90)
    elif filter_option == "Últimos 6 Meses":
        df_filtered = df.tail(180)
    elif filter_option == "Último Año":
        df_filtered = df.tail(365)
    else:
        df_filtered = df
    
    # Métricas generales
    st.subheader("📊 Estadísticas del Período Seleccionado")
    
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    
    metric_col1.metric("Precio Actual", f"${df_filtered['close'].iloc[-1]:,.2f}")
    metric_col2.metric("Máximo", f"${df_filtered['high'].max():,.2f}")
    metric_col3.metric("Mínimo", f"${df_filtered['low'].min():,.2f}")
    metric_col4.metric("Promedio", f"${df_filtered['close'].mean():,.2f}")
    
    # Calcular cambio porcentual del período
    change_pct = ((df_filtered['close'].iloc[-1] - df_filtered['close'].iloc[0]) / 
                  df_filtered['close'].iloc[0] * 100)
    metric_col5.metric("Cambio del Período", f"{change_pct:.2f}%", 
                      delta=f"{change_pct:.2f}%", 
                      delta_color="normal")
    
    # Gráfico principal
    st.subheader("📈 Gráfico de Precios Interactivo")
    fig_explore = create_candlestick_chart(df_filtered, f"Bitcoin - {filter_option}")
    st.plotly_chart(fig_explore, use_container_width=True)
    
    # Análisis adicional
    st.subheader("📊 Análisis Detallado")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.markdown("#### 📈 Volatilidad")
        volatility_7 = df_filtered['close'].pct_change().rolling(window=7).std() * 100
        volatility_30 = df_filtered['close'].pct_change().rolling(window=30).std() * 100
        
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=volatility_7,
            name='Volatilidad 7 días',
            line=dict(color='orange')
        ))
        if len(df_filtered) >= 30:
            fig_vol.add_trace(go.Scatter(
                x=df_filtered['date'],
                y=volatility_30,
                name='Volatilidad 30 días',
                line=dict(color='red')
            ))
        fig_vol.update_layout(
            title="Volatilidad Histórica",
            xaxis_title="Fecha",
            yaxis_title="Volatilidad (%)",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_vol, use_container_width=True)
    
    with analysis_col2:
        st.markdown("#### 📊 Distribución de Retornos")
        returns = df_filtered['close'].pct_change() * 100
        
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=returns.dropna(),
            nbinsx=50,
            name='Retornos Diarios',
            marker_color='steelblue'
        ))
        fig_dist.update_layout(
            title="Distribución de Retornos Diarios",
            xaxis_title="Retorno (%)",
            yaxis_title="Frecuencia",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Tabla de datos
    st.subheader("📋 Datos Tabulares")
    with st.expander("Ver Datos Completos"):
        st.dataframe(
            df_filtered[['date', 'open', 'high', 'low', 'close', 'volume']]
            .style.format({
                'open': '${:,.2f}',
                'high': '${:,.2f}',
                'low': '${:,.2f}',
                'close': '${:,.2f}',
                'volume': '{:,.0f}'
            }),
            use_container_width=True
        )

# ==================== TAB MODELO ====================
with tab_modelo:
    st.header("🧠 Sobre el Modelo de Machine Learning")
    
    # Información del modelo
    st.subheader("📊 Información General del Modelo")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("""
        <div class="metric-card">
        <h4>Tipo de Modelo</h4>
        <p style="font-size: 1.5rem; font-weight: bold;">Decision Tree Regressor</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>Features Totales</h4>
        <p style="font-size: 1.5rem; font-weight: bold;">{len(FEATURE_NAMES)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with info_col3:
        st.markdown(f"""
        <div class="metric-card">
        <h4>Lags Temporales</h4>
        <p style="font-size: 1.5rem; font-weight: bold;">{N_LAGS}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Descripción del modelo
    st.markdown("---")
    st.subheader("🎯 ¿Qué es un Decision Tree Regressor?")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        Un **Decision Tree Regressor** es un algoritmo de machine learning que:
        
        - 🌳 Crea un árbol de decisiones para predecir valores continuos
        - 📊 Divide los datos en ramas basándose en features importantes
        - 🎯 Encuentra patrones no lineales en los datos históricos
        - ⚡ Es rápido y eficiente para predicciones en tiempo real
        
        #### Ventajas:
        - ✅ Captura relaciones no lineales complejas
        - ✅ No requiere normalización de datos
        - ✅ Fácil de interpretar y visualizar
        - ✅ Robusto a outliers
        
        #### Limitaciones:
        - ⚠️ Puede sobreajustarse (overfitting)
        - ⚠️ Sensible a pequeños cambios en los datos
        - ⚠️ No extrapola bien fuera del rango de entrenamiento
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>🔧 Configuración del Modelo</h4>
        <ul>
        <li><b>Retroalimentación:</b> {}</li>
        <li><b>Scaler Target:</b> {}</li>
        <li><b>Features Base:</b> {}</li>
        </ul>
        </div>
        """.format(
            "Activada ✅" if USE_FEEDBACK else "Desactivada ❌",
            "Sí" if SCALER_Y is not None else "No",
            ", ".join(BASE_FEATURES)
        ), unsafe_allow_html=True)
    
    # Features del modelo
    st.markdown("---")
    st.subheader("🎨 Features Utilizadas por el Modelo")
    
    st.markdown("""
    El modelo utiliza las siguientes categorías de features para hacer sus predicciones:
    """)
    
    feature_categories = {
        "💹 Cambios Porcentuales": [f for f in FEATURE_NAMES if "_pct" in f and "lag" not in f],
        "⏱️ Lags Temporales": [f for f in FEATURE_NAMES if "lag" in f],
        "📊 Medias Móviles": [f for f in FEATURE_NAMES if "ma" in f.lower()],
        "📉 Volatilidad": [f for f in FEATURE_NAMES if "volatilidad" in f or "vol" in f],
        "🔄 Retroalimentación": [f for f in FEATURE_NAMES if "prev" in f]
    }
    
    for category, features in feature_categories.items():
        if features:
            with st.expander(f"{category} ({len(features)} features)"):
                for i, feat in enumerate(features, 1):
                    st.text(f"{i}. {feat}")
    
    # Lista completa de features
    with st.expander("📋 Ver Lista Completa de Features"):
        feature_df = pd.DataFrame({
            "N°": range(1, len(FEATURE_NAMES) + 1),
            "Feature": FEATURE_NAMES
        })
        st.dataframe(feature_df, use_container_width=True)
    
    # Explicación técnica
    st.markdown("---")
    st.subheader("🔬 Explicación Técnica del Proceso")
    
    st.markdown("""
    ### 📝 Pipeline de Predicción
    
    1. **Preprocesamiento de Datos**
       - Carga de datos históricos (OHLCV)
       - Conversión de fechas y ordenamiento temporal
       - Cálculo de retornos porcentuales (multiplicados por 100)
    
    2. **Ingeniería de Features**
       - Cálculo de cambios porcentuales para OHLC
       - Generación de lags temporales (últimos N períodos)
       - Cálculo de medias móviles (MA3, MA7)
       - Cálculo de volatilidad (desviación estándar de 7 períodos)
       - Features de retroalimentación (si está activada)
    
    3. **Preparación para Predicción**
       - Selección de las últimas N observaciones
       - Eliminación de filas con valores faltantes (NaN)
       - Asegurar el orden correcto de features
       - Normalización con scaler (si aplica)
    
    4. **Predicción**
       - Envío de features al modelo Decision Tree
       - Obtención de predicción (cambio porcentual)
       - Desescalado si se usó StandardScaler
       - Cálculo del precio predicho
    
    5. **Post-procesamiento**
       - Actualización de features de retroalimentación
       - Generación de visualizaciones
       - Cálculo de métricas adicionales
    
    ### 🔄 Retroalimentación del Modelo
    
    Cuando está activada, el modelo utiliza información de predicciones anteriores:
    - **prev_pred**: Predicción del período anterior
    - **prev_err**: Error de la predicción anterior (predicción - valor real)
    
    Esto permite al modelo "aprender" de sus errores recientes y ajustar predicciones futuras.
    """)
    
    # Recomendaciones
    st.markdown("---")
    st.subheader("💡 Recomendaciones de Uso")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        <div class="info-box">
        <h4>✅ Mejores Prácticas</h4>
        <ul>
        <li>Usa al menos 300-400 registros históricos</li>
        <li>Compara predicciones a diferentes plazos</li>
        <li>Considera el contexto del mercado</li>
        <li>Combina con otros análisis (fundamental, técnico)</li>
        <li>Monitorea la volatilidad del mercado</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="warning-box">
        <h4>⚠️ Precauciones</h4>
        <ul>
        <li>No uses solo este modelo para inversiones reales</li>
        <li>El modelo puede fallar en mercados extremos</li>
        <li>Las predicciones de largo plazo son menos confiables</li>
        <li>Siempre considera el riesgo en tus decisiones</li>
        <li>Reevalúa el modelo periódicamente</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><b>Bitcoin Price Predictor</b> | Desarrollado con Streamlit y Machine Learning</p>
    <p>Para fines educativos y de investigación únicamente</p>
</div>
""", unsafe_allow_html=True)
