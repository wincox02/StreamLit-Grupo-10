# 🚀 INSTRUCCIONES PARA DESPLIEGUE EN STREAMLIT CLOUD

## ✅ CAMBIOS REALIZADOS

1. **Archivo principal renombrado:**
   - `main_mejorado.py` → `main.py` (archivo principal)
   - `main.py` (original) → `main_original_backup.py` (backup)

2. **Problema resuelto:**
   - Error: `NameError: name 'alt' is not defined`
   - Causa: El archivo original usaba Altair sin importarlo
   - Solución: Ahora `main.py` es la versión mejorada con Plotly

## 📋 VERIFICACIÓN PRE-DESPLIEGUE

### Archivos Requeridos
- [x] `main.py` (versión mejorada - 39KB)
- [x] `requirements.txt` (con plotly incluido)
- [x] `models/model_feedback.pkl` (modelo)
- [x] Archivos CSV de datos (BTCUSDT_1d_last_year.csv, etc.)

### Dependencias en requirements.txt
```
streamlit
pandas
numpy
scikit-learn
plotly  ← IMPORTANTE: Necesario para gráficos
joblib
```

## 🌐 PASOS PARA DESPLEGAR EN STREAMLIT CLOUD

### 1. Preparación del Repositorio
```bash
# Asegúrate de que estos archivos estén en el repositorio:
git add main.py
git add requirements.txt
git add models/model_feedback.pkl
git add *.csv
git commit -m "Aplicación mejorada con todas las correcciones"
git push
```

### 2. Configuración en Streamlit Cloud
1. Ve a https://share.streamlit.io/
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Main file path:** `main.py`
   - **Python version:** 3.9 o superior
   - Todo lo demás en default

### 3. Verificación Post-Despliegue
- [ ] La app carga sin errores
- [ ] Los 4 tabs son visibles
- [ ] Los gráficos son interactivos (Plotly)
- [ ] Las predicciones funcionan
- [ ] No hay errores de `alt` o `altair`

## 🔧 TROUBLESHOOTING

### Error: "No module named 'plotly'"
**Solución:** Verifica que `requirements.txt` contenga `plotly`

### Error: "No se encontró el modelo"
**Solución:** Asegúrate de que `models/model_feedback.pkl` esté en el repo

### Error: "No se encontró archivo CSV"
**Solución:** Sube al menos un archivo CSV al repositorio

### Los gráficos no se ven
**Solución:** 
1. Verifica que Plotly esté instalado
2. Limpia el caché de Streamlit Cloud
3. Redeploy la aplicación

## 📊 CARACTERÍSTICAS ACTIVAS

Una vez desplegado, tendrás:

### ✅ Tab "🏠 Inicio"
- Explicación del modelo
- Guía de uso
- Advertencias

### ✅ Tab "📈 Predicción"
- Botón "Predecir Mañana"
- Botón "Predicción Múltiples Días" (1-30 días)
- Comparación a 1, 5 y 10 días
- Gráficos interactivos con zoom

### ✅ Tab "🔍 Exploración de Datos"
- Filtros temporales
- Gráficos de velas (candlestick)
- Análisis de volatilidad
- Distribución de retornos

### ✅ Tab "🧠 Sobre el Modelo"
- Información técnica
- Features utilizadas
- Pipeline de predicción
- Mejores prácticas

## 🎯 URLs DEL PROYECTO

Una vez desplegado, tu app estará en:
```
https://[tu-usuario]-streamlit-grupo-10-main-[hash].streamlit.app
```

## 📝 NOTAS IMPORTANTES

1. **No uses los scripts .bat en la nube** (son solo para uso local)
2. **El archivo principal es `main.py`** (ya está correctamente nombrado)
3. **Todos los gráficos usan Plotly** (no Altair)
4. **El sidebar está oculto** (interfaz limpia)
5. **Todas las 10 correcciones están implementadas**

## ✅ CHECKLIST FINAL

Antes de desplegar, verifica:

- [x] `main.py` es la versión mejorada (39KB aprox)
- [x] `requirements.txt` incluye `plotly`
- [x] El modelo `models/model_feedback.pkl` existe
- [x] Al menos un archivo CSV de datos existe
- [x] No hay referencias a `altair` en main.py
- [x] El README.md está actualizado
- [x] Todos los archivos están en el repositorio

## 🎉 ¡LISTO PARA DESPLEGAR!

Si todo está marcado, puedes hacer push a GitHub y desplegar en Streamlit Cloud sin problemas.

---

**Fecha:** Noviembre 10, 2025
**Estado:** ✅ LISTO PARA PRODUCCIÓN
