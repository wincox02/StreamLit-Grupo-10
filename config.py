# Configuración de la Aplicación Bitcoin Predictor
# Puedes modificar estos valores para personalizar la aplicación

# ==================== CONFIGURACIÓN DEL MODELO ====================

# Ruta al modelo pre-entrenado
MODEL_PATH = "models/model_feedback.pkl"

# ==================== CONFIGURACIÓN DE DATOS ====================

# Archivo CSV por defecto (si no se sube uno)
DEFAULT_CSV = "BTCUSDT_1d_last_year.csv"

# Número de registros históricos por defecto
DEFAULT_N_RECENT_SIMPLE = 400  # Para predicción simple
DEFAULT_N_RECENT_MULTI = 400   # Para predicción múltiple

# ==================== CONFIGURACIÓN DE PREDICCIÓN ====================

# Días por defecto para predicción múltiple
DEFAULT_PREDICTION_DAYS = 7

# Rango de días permitido para predicción múltiple
MIN_PREDICTION_DAYS = 1
MAX_PREDICTION_DAYS = 30

# Rango de registros históricos permitido
MIN_RECENT_RECORDS = 100
MAX_RECENT_RECORDS = 1000
STEP_RECENT_RECORDS = 50

# ==================== CONFIGURACIÓN DE VISUALIZACIÓN ====================

# Altura de gráficos (en píxeles)
CHART_HEIGHT_MAIN = 700        # Gráfico principal
CHART_HEIGHT_COMPARISON = 600  # Gráfico de comparación
CHART_HEIGHT_ANALYSIS = 400    # Gráficos de análisis

# Colores para gráficos
COLOR_BULLISH = "#26a69a"      # Verde para velas alcistas
COLOR_BEARISH = "#ef5350"      # Rojo para velas bajistas
COLOR_PREDICTION = "red"        # Color de línea de predicción
COLOR_MA7 = "orange"           # Media móvil 7 días
COLOR_MA30 = "blue"            # Media móvil 30 días

# Estilo de línea de predicción
PREDICTION_LINE_WIDTH = 3
PREDICTION_LINE_DASH = "dash"

# ==================== CONFIGURACIÓN DE FILTROS ====================

# Opciones de filtros temporales
FILTER_OPTIONS = [
    "Última Semana",
    "Último Mes",
    "Últimos 3 Meses",
    "Últimos 6 Meses",
    "Último Año",
    "Todo"
]

# Mapeo de filtros a días
FILTER_DAYS = {
    "Última Semana": 7,
    "Último Mes": 30,
    "Últimos 3 Meses": 90,
    "Últimos 6 Meses": 180,
    "Último Año": 365,
    "Todo": None  # Muestra todo
}

# ==================== CONFIGURACIÓN DE MEDIAS MÓVILES ====================

# Períodos de medias móviles
MA_SHORT = 7   # Media móvil corta
MA_LONG = 30   # Media móvil larga

# Mínimo de datos necesarios para calcular cada MA
MIN_DATA_MA_SHORT = 7
MIN_DATA_MA_LONG = 30

# ==================== CONFIGURACIÓN DE VOLATILIDAD ====================

# Ventanas para cálculo de volatilidad
VOLATILITY_WINDOW_SHORT = 7
VOLATILITY_WINDOW_LONG = 30

# ==================== CONFIGURACIÓN DE RETROALIMENTACIÓN ====================

# Activar/desactivar retroalimentación por defecto
DEFAULT_USE_FEEDBACK = True

# ==================== CONFIGURACIÓN DE PÁGINA ====================

# Título de la página
PAGE_TITLE = "Bitcoin Predictor - Análisis y Predicción"
PAGE_ICON = "₿"
LAYOUT = "wide"

# ==================== CONFIGURACIÓN DE TABS ====================

# Nombres de los tabs
TAB_NAMES = [
    "🏠 Inicio",
    "📈 Predicción",
    "🔍 Exploración de Datos",
    "🧠 Sobre el Modelo"
]

# ==================== MENSAJES Y TEXTOS ====================

# Mensaje de advertencia principal
WARNING_MESSAGE = """
⚠️ Este modelo es solo para fines educativos y de investigación. 
NO debe utilizarse como única base para decisiones de inversión.
"""

# Mensaje de éxito en predicción
SUCCESS_MESSAGE_PREDICTION = "✅ Predicción Completada"

# Mensaje de error genérico
ERROR_MESSAGE_GENERIC = "❌ Error: {}"

# ==================== CONFIGURACIÓN DE FORMATO ====================

# Formato de números
PRICE_FORMAT = "${:,.2f}"
PERCENT_FORMAT = "{:.3f}%"
NUMBER_FORMAT = "{:,.0f}"

# ==================== CONFIGURACIÓN DE EXPORTACIÓN ====================

# Activar/desactivar opciones de exportación
ENABLE_EXPORT_CSV = False  # Por ahora desactivado
ENABLE_EXPORT_PNG = False  # Por ahora desactivado

# ==================== CONFIGURACIÓN AVANZADA ====================

# Mostrar opciones avanzadas por defecto
SHOW_ADVANCED_OPTIONS = False

# Mostrar información de debug
DEBUG_MODE = False

# ==================== NOTAS ====================
"""
Para aplicar estos cambios:
1. Modifica los valores en este archivo
2. Importa estas constantes en main_mejorado.py
3. Reemplaza los valores hardcodeados con estas constantes

Ejemplo de uso en main_mejorado.py:
    from config import MODEL_PATH, DEFAULT_CSV, PAGE_TITLE
    
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )
"""
