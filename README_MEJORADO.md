# Bitcoin Price Predictor - Aplicación Mejorada

## 🚀 Mejoras Implementadas

### ✅ Correcciones Realizadas

1. **✅ Eliminado el sidebar izquierdo** - La interfaz ahora es más limpia y centrada en el contenido principal
2. **✅ Gráficos interactivos con zoom** - Usando Plotly para gráficos tipo trading con zoom y filtros
3. **✅ Botón "Predecir Mañana"** - Muestra los datos enviados al modelo y la predicción
4. **✅ Botón "Predicción Múltiples Días"** - Usa retroalimentación para predecir varios días
5. **✅ Pantalla inicial explicativa** - Tab de inicio con explicación completa del modelo
6. **✅ Interactividad con filtros** - Filtros temporales y opciones de visualización
7. **✅ Gráficos tipo velas (candlestick)** - Visualización profesional tipo trading
8. **✅ Tab de exploración del modelo** - Métricas, features y explicaciones técnicas
9. **✅ Comparación de predicciones** - Compara predicciones a 1, 5 y 10 días

## 📋 Características Principales

### 🏠 Tab Inicio
- Explicación completa de qué hace la aplicación
- Guía de cómo usar cada funcionalidad
- Información sobre el modelo y sus características
- Advertencias y recomendaciones de uso

### 📈 Tab Predicción
- **Predicción de Mañana**: 
  - Botón dedicado para predecir el próximo día
  - Muestra las features enviadas al modelo (opcional)
  - Visualización con gráfico de velas interactivo
  - Métricas claras del cambio predicho

- **Predicción Múltiples Días**:
  - Configurable de 1 a 30 días
  - Usa retroalimentación de predicciones anteriores
  - Tabla detallada con todas las predicciones
  - Gráfico que muestra la extensión de la línea de predicción
  - Estadísticas de las predicciones

- **Comparación de Predicciones**:
  - Botón para generar comparación completa (1, 5 y 10 días)
  - Gráfico comparativo de diferentes plazos
  - Permite limpiar las predicciones

### 🔍 Tab Exploración de Datos
- Filtros temporales: Última semana, mes, 3 meses, 6 meses, año, todo
- Gráficos de velas interactivos con zoom
- Estadísticas del período seleccionado
- Análisis de volatilidad
- Distribución de retornos
- Tabla de datos completa

### 🧠 Tab Sobre el Modelo
- Información general del Decision Tree Regressor
- Explicación de ventajas y limitaciones
- Lista completa de features por categorías
- Explicación técnica del pipeline de predicción
- Información sobre la retroalimentación del modelo
- Mejores prácticas y precauciones

## 🛠️ Instalación y Uso

### Requisitos
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación Mejorada
```bash
streamlit run main_mejorado.py
```

### Ejecutar la Aplicación Original (si lo necesitas)
```bash
streamlit run main.py
```

## 📊 Estructura de Archivos

```
├── main_mejorado.py          # ✨ Nueva versión mejorada (USAR ESTE)
├── main.py                    # Versión original (backup)
├── app.py                     # Otra versión de entrenamiento
├── requirements.txt           # Dependencias actualizadas con plotly
├── models/
│   └── model_feedback.pkl     # Modelo pre-entrenado
├── data/
│   └── sample_binance.csv     # Datos de ejemplo
├── src/
│   └── features.py            # Utilidades para features
└── *.csv                      # Datos históricos de Bitcoin
```

## 🎯 Cómo Usar la Aplicación

### 1. Inicio
- Lee la explicación del modelo y sus características
- Revisa las advertencias y recomendaciones
- Familiarízate con la guía de uso

### 2. Explorar Datos
- Ve al tab "Exploración de Datos"
- Selecciona el período que quieres visualizar
- Analiza los gráficos interactivos con zoom
- Revisa las estadísticas y análisis de volatilidad

### 3. Hacer Predicciones

#### Predicción Simple (Mañana)
1. Ve al tab "Predicción"
2. En la columna izquierda, configura opciones avanzadas si lo deseas
3. Haz clic en "🎯 Predecir Mañana"
4. Revisa las métricas y el gráfico interactivo

#### Predicción Múltiple (Varios Días)
1. Ve al tab "Predicción"
2. En la columna derecha, selecciona el número de días (1-30)
3. Haz clic en "📊 Predecir Múltiples Días"
4. Revisa la tabla de predicciones y el gráfico

#### Comparación de Predicciones
1. Ve a la sección "Comparación de Predicciones"
2. Haz clic en "🔄 Generar Comparación Completa"
3. Observa el gráfico comparativo con 1, 5 y 10 días
4. Analiza las diferencias entre plazos

### 4. Entender el Modelo
- Ve al tab "Sobre el Modelo"
- Lee sobre el Decision Tree Regressor
- Revisa las features utilizadas
- Estudia el pipeline técnico de predicción
- Lee las mejores prácticas

## 🎨 Características de los Gráficos

### Interactividad
- **Zoom**: Arrastra para hacer zoom en un área específica
- **Pan**: Haz clic y arrastra para mover el gráfico
- **Hover**: Pasa el mouse para ver detalles
- **Reset**: Doble clic para resetear el zoom
- **Leyenda**: Haz clic en la leyenda para mostrar/ocultar series

### Gráficos de Velas (Candlestick)
- **Verde**: Día con cierre superior al apertura (alcista)
- **Rojo**: Día con cierre inferior al apertura (bajista)
- **Medias Móviles**: MA7 (naranja) y MA30 (azul)
- **Volumen**: Barras en la parte inferior
- **Predicciones**: Línea roja discontinua con estrellas

## 📈 Métricas y Estadísticas

### Métricas de Predicción
- **Cambio Predicho**: Porcentaje de cambio esperado
- **Precio Actual**: Último precio de cierre conocido
- **Precio Predicho**: Precio esperado basado en la predicción
- **Delta**: Diferencia en dólares entre actual y predicho

### Estadísticas de Múltiples Días
- **Cambio Promedio**: Media de los cambios predichos
- **Cambio Máximo**: Mayor cambio predicho
- **Cambio Mínimo**: Menor cambio predicho
- **Desviación Estándar**: Variabilidad de las predicciones

## ⚠️ Notas Importantes

### Advertencias
1. **Solo para fines educativos**: No usar como única base para inversiones
2. **Volatilidad del mercado**: El modelo puede fallar en condiciones extremas
3. **Predicciones de largo plazo**: Menos confiables a medida que aumentan los días
4. **Contexto del mercado**: Siempre considerar noticias y eventos externos

### Limitaciones del Modelo
- No captura eventos extraordinarios (noticias, regulaciones, etc.)
- Asume que los patrones históricos se repetirán
- Sensible a cambios bruscos en el mercado
- Las predicciones múltiples acumulan incertidumbre

## 🔧 Personalización

### Cambiar el Modelo
Reemplaza el archivo `models/model_feedback.pkl` con tu propio modelo entrenado.

### Cambiar los Datos
Coloca tu CSV en la raíz con el nombre `BTCUSDT_1d_last_year.csv` o usa el uploader en la app.

### Ajustar Parámetros
Modifica las siguientes variables en `main_mejorado.py`:
- `n_recent_simple`: Registros para predicción simple (default: 400)
- `n_recent_multi`: Registros para predicción múltiple (default: 400)
- `n_days_predict`: Días a predecir (default: 7)

## 📞 Soporte

Para problemas o sugerencias, consulta con el equipo de desarrollo.

## 📝 Changelog

### Versión 2.0 (Mejorada)
- ✅ Eliminado sidebar, interfaz más limpia
- ✅ Gráficos Plotly interactivos con zoom
- ✅ Botones dedicados para predicciones
- ✅ Comparación de predicciones a múltiples plazos
- ✅ Tab de inicio con explicaciones completas
- ✅ Tab de exploración con filtros avanzados
- ✅ Tab del modelo con información técnica
- ✅ Gráficos de velas tipo trading
- ✅ Retroalimentación en predicciones múltiples
- ✅ Estadísticas y métricas mejoradas

### Versión 1.0 (Original)
- Predicción básica con Decision Tree
- Gráficos Altair estáticos
- Sidebar con opciones

---

**Desarrollado con ❤️ usando Streamlit, Plotly y Machine Learning**
