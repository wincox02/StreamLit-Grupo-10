# 🚀 Guía Rápida de Uso

## ⚡ Instalación Rápida

### Opción 1: Usar el script de instalación
1. Haz doble clic en `setup.bat`
2. Espera a que se instalen las dependencias
3. ¡Listo!

### Opción 2: Instalación manual
```bash
pip install -r requirements.txt
```

## 🎮 Ejecutar la Aplicación

### Opción 1: Usar el script de ejecución
1. Haz doble clic en `ejecutar.bat`
2. Se abrirá automáticamente en tu navegador

### Opción 2: Ejecución manual
```bash
streamlit run main_mejorado.py
```

## 📱 Navegación por la Aplicación

### Tab 1: 🏠 Inicio
**¿Qué encontrarás?**
- Explicación completa del sistema
- Guía de cómo usar cada funcionalidad
- Advertencias importantes
- Información del modelo

**¿Qué hacer?**
- Lee esta sección primero para entender cómo funciona todo
- Revisa las características principales
- Lee las advertencias antes de usar el sistema

---

### Tab 2: 📈 Predicción

#### Sección 1: Predicción de Mañana (Columna Izquierda)
**¿Para qué sirve?**
- Predecir solo el próximo día
- Ver exactamente qué datos usa el modelo

**Pasos:**
1. (Opcional) Expande "⚙️ Configuración Avanzada"
2. Ajusta el número de registros históricos a usar
3. Marca "Mostrar features" si quieres ver los datos enviados
4. Haz clic en "🎯 Predecir Mañana"
5. Revisa las métricas y el gráfico

**Métricas que verás:**
- **Cambio Predicho**: Porcentaje esperado (ej: +2.5% o -1.3%)
- **Precio Actual**: Último precio conocido
- **Precio Predicho**: Precio esperado para mañana

#### Sección 2: Predicción Múltiples Días (Columna Derecha)
**¿Para qué sirve?**
- Predecir varios días hacia adelante (1-30 días)
- Ver la tendencia extendida en el gráfico

**Pasos:**
1. Expande "⚙️ Configuración Avanzada"
2. Ajusta "Días a predecir" (deslizador de 1 a 30)
3. Marca "Mostrar detalles" si quieres ver estadísticas
4. Haz clic en "📊 Predecir Múltiples Días"
5. Revisa la tabla y el gráfico

**¿Qué muestra?**
- Tabla con predicciones día por día
- Gráfico con línea extendida de predicciones
- Estadísticas (promedio, máximo, mínimo, desviación)

#### Sección 3: Comparación de Predicciones
**¿Para qué sirve?**
- Comparar predicciones a 1, 5 y 10 días simultáneamente
- Ver cómo divergen las predicciones de diferentes plazos

**Pasos:**
1. Haz clic en "🔄 Generar Comparación Completa"
2. Espera a que se generen las 3 predicciones
3. Observa el gráfico comparativo
4. Analiza las diferencias entre plazos

**Consejo:** Las predicciones de corto plazo (1 día) suelen ser más precisas que las de largo plazo (10 días)

---

### Tab 3: 🔍 Exploración de Datos

**¿Para qué sirve?**
- Ver datos históricos de Bitcoin
- Analizar tendencias y patrones
- Estudiar volatilidad

**Pasos:**
1. Selecciona el período: Última semana, mes, 3 meses, etc.
2. Marca/desmarca "Mostrar Medias Móviles" y "Mostrar Volumen"
3. Observa las estadísticas del período
4. Interactúa con el gráfico:
   - **Zoom**: Arrastra un área con el mouse
   - **Pan**: Clic y arrastra para mover
   - **Reset**: Doble clic
5. Revisa los gráficos de volatilidad y distribución
6. (Opcional) Expande "Ver Datos Completos" para la tabla

**Gráficos disponibles:**
- **Principal**: Velas japonesas con volumen
- **Volatilidad**: Histórico de volatilidad 7 y 30 días
- **Distribución**: Histograma de retornos diarios

---

### Tab 4: 🧠 Sobre el Modelo

**¿Para qué sirve?**
- Entender cómo funciona el modelo
- Ver qué features utiliza
- Conocer limitaciones y recomendaciones

**Secciones:**
1. **Información General**: Tipo de modelo, número de features, etc.
2. **Explicación del Decision Tree**: Ventajas y limitaciones
3. **Features Utilizadas**: Lista completa por categorías
4. **Explicación Técnica**: Pipeline de predicción paso a paso
5. **Recomendaciones**: Mejores prácticas y precauciones

**Consejo:** Lee esta sección para entender mejor las predicciones

---

## 💡 Tips y Trucos

### Para Predicciones Más Precisas
1. ✅ Usa al menos 300-400 registros históricos
2. ✅ Compara predicciones de diferentes plazos
3. ✅ Considera el contexto del mercado (noticias, eventos)
4. ✅ Revisa la volatilidad reciente en el tab de exploración

### Para Mejor Visualización
1. 🔍 Usa el zoom en los gráficos para ver detalles
2. 🔍 Pasa el mouse sobre las velas para ver valores exactos
3. 🔍 Haz clic en la leyenda para mostrar/ocultar series
4. 🔍 Usa los filtros temporales para comparar períodos

### Interpretación de Resultados
- **Cambio positivo (+)**: Predicción de subida de precio
- **Cambio negativo (-)**: Predicción de bajada de precio
- **Volatilidad alta**: Mayor incertidumbre en la predicción
- **Volatilidad baja**: Mayor confianza en la predicción

---

## ⚠️ Advertencias Importantes

### 🚫 NO hacer:
- ❌ NO uses SOLO este modelo para invertir dinero real
- ❌ NO ignores las condiciones del mercado
- ❌ NO asumas que el pasado predice el futuro perfectamente
- ❌ NO confíes ciegamente en predicciones de largo plazo

### ✅ SÍ hacer:
- ✅ Usa el modelo como UNA herramienta más de análisis
- ✅ Combina con análisis fundamental y técnico
- ✅ Considera el contexto (noticias, regulaciones, etc.)
- ✅ Verifica las predicciones con otras fuentes
- ✅ Entiende las limitaciones del modelo

---

## 🆘 Solución de Problemas

### Error: "No se encontró el modelo"
**Solución:** Asegúrate de que existe el archivo `models/model_feedback.pkl`

### Error: "No se encontró archivo CSV"
**Solución:** 
- Coloca un archivo CSV en la raíz llamado `BTCUSDT_1d_last_year.csv`
- O usa el uploader de archivos en la app

### La aplicación no se abre
**Solución:**
1. Verifica que instalaste las dependencias: `pip install -r requirements.txt`
2. Verifica que Streamlit esté instalado: `pip list | findstr streamlit`
3. Intenta ejecutar manualmente: `streamlit run main_mejorado.py`

### Los gráficos no se ven bien
**Solución:**
1. Actualiza tu navegador
2. Verifica que Plotly esté instalado: `pip list | findstr plotly`
3. Reinstala Plotly: `pip install --upgrade plotly`

---

## 📊 Interpretación de Gráficos

### Gráfico de Velas (Candlestick)
- **Vela Verde**: Precio cerró más alto que abrió (alcista)
- **Vela Roja**: Precio cerró más bajo que abrió (bajista)
- **Sombra Superior**: Precio máximo del día
- **Sombra Inferior**: Precio mínimo del día
- **Cuerpo**: Diferencia entre apertura y cierre

### Líneas de Predicción
- **Línea Roja Discontinua**: Predicción del modelo
- **Estrellas Rojas**: Puntos predichos
- **Línea Verde/Naranja/Roja**: Comparación de plazos (1/5/10 días)

### Gráfico de Volatilidad
- **Línea Alta**: Mayor incertidumbre/riesgo
- **Línea Baja**: Menor incertidumbre/riesgo
- **Picos**: Momentos de alta volatilidad (eventos importantes)

---

## 🎓 Glosario de Términos

- **OHLC**: Open (Apertura), High (Máximo), Low (Mínimo), Close (Cierre)
- **Retorno**: Cambio porcentual en el precio
- **Lag**: Valor de un período anterior (ej: lag1 = valor de ayer)
- **Media Móvil (MA)**: Promedio de los últimos N períodos
- **Volatilidad**: Medida de variabilidad del precio
- **Retroalimentación**: El modelo aprende de predicciones anteriores
- **Feature**: Variable que el modelo usa para predecir
- **Decision Tree**: Algoritmo de ML basado en árbol de decisiones

---

## 📞 Contacto y Soporte

Para preguntas, problemas o sugerencias, contacta al equipo de desarrollo.

---

**¡Disfruta prediciendo Bitcoin! 🚀₿**
