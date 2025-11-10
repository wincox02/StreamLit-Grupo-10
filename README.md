# Bitcoin Price Predictor - Aplicación Mejorada

Aplicación de predicción de precios de Bitcoin usando Machine Learning con interfaz interactiva.

## 🚀 Despliegue en Streamlit Cloud

### ✅ Archivo Principal
- **`main.py`** - Aplicación mejorada completa (USAR ESTE)
- `main_original_backup.py` - Backup del original

### 📦 Dependencias (requirements.txt)
```
streamlit
pandas
numpy
scikit-learn
plotly
joblib
```

### 📁 Estructura del Proyecto
```
├── main.py (✅ Aplicación mejorada - principal)
├── main_original_backup.py (Backup)
├── requirements.txt
├── models/
│   └── model_feedback.pkl
├── data/
└── *.csv (datos históricos de Bitcoin)
```

## 🎯 Características

### 🏠 Tab Inicio
- Explicación completa del modelo
- Guía de uso
- Advertencias importantes

### 📈 Tab Predicción
- **Predicción de Mañana**: Predice el próximo día
- **Predicción Múltiples Días**: 1-30 días con retroalimentación
- **Comparación**: Visualiza predicciones a 1, 5 y 10 días

### 🔍 Tab Exploración
- Filtros temporales (semana, mes, 3m, 6m, año)
- Gráficos de velas interactivos con zoom
- Análisis de volatilidad
- Distribución de retornos

### 🧠 Tab Sobre el Modelo
- Información técnica del Decision Tree
- Features utilizadas
- Pipeline de predicción
- Mejores prácticas

## 🎨 Mejoras Implementadas

✅ Sin sidebar (interfaz limpia)
✅ Gráficos interactivos con Plotly
✅ Zoom, pan y tooltips
✅ Gráficos de velas tipo trading
✅ Predicciones con retroalimentación
✅ Comparación de múltiples plazos
✅ Filtros avanzados
✅ Documentación completa

## 📝 Notas para Streamlit Cloud

1. **Archivo de entrada**: `main.py` (ya renombrado)
2. **Instalación automática**: Streamlit Cloud instala `requirements.txt`
3. **No se necesitan scripts .bat**: Solo para uso local
4. **Puerto por defecto**: 8501

## 📚 Documentación Adicional

Para más información, consulta:
- `README_MEJORADO.md` - Documentación completa
- `GUIA_RAPIDA.md` - Guía de uso
- `EJEMPLOS_USO.md` - Casos prácticos

## ⚠️ Advertencia

Esta aplicación es solo para fines educativos y de investigación. 
No debe utilizarse como única base para decisiones de inversión.

---

**Versión:** 2.0 (Mejorada)
**Última actualización:** Noviembre 2025
