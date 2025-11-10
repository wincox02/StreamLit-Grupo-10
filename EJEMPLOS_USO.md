# 🎓 EJEMPLOS DE USO Y CASOS PRÁCTICOS

## 📚 Índice
1. [Uso Básico](#uso-básico)
2. [Casos de Uso Comunes](#casos-de-uso-comunes)
3. [Interpretación de Resultados](#interpretación-de-resultados)
4. [Troubleshooting](#troubleshooting)
5. [Personalización](#personalización)

---

## 🚀 Uso Básico

### Ejemplo 1: Predicción Simple de Mañana

**Escenario:** Quieres saber si Bitcoin subirá o bajará mañana.

**Pasos:**
1. Abre la aplicación: `streamlit run main_mejorado.py`
2. Ve al tab "📈 Predicción"
3. Haz clic en "🎯 Predecir Mañana"
4. Lee el resultado:
   - Si el cambio es positivo (+2.5%): Se espera subida
   - Si el cambio es negativo (-1.3%): Se espera bajada

**Resultado Esperado:**
```
✅ Predicción Completada

Cambio Predicho: +2.345%
Precio Actual: $45,234.50
Precio Predicho: $46,295.21
Delta: +$1,060.71
```

**Interpretación:**
- El modelo predice una subida del 2.345%
- Precio actual: $45,234.50
- Precio esperado mañana: $46,295.21
- Ganancia esperada: $1,060.71 por Bitcoin

---

### Ejemplo 2: Predicción de una Semana

**Escenario:** Quieres ver la tendencia de la próxima semana.

**Pasos:**
1. Ve al tab "📈 Predicción"
2. En la columna derecha, expande "⚙️ Configuración Avanzada"
3. Ajusta "Días a predecir" a 7
4. Haz clic en "📊 Predecir Múltiples Días"

**Resultado Esperado:**
```
Tabla de Predicciones:

Día | Fecha        | Cambio (%) | Precio ($)
----|--------------|------------|-------------
1   | 2025-11-11   | +1.234%    | $45,791.23
2   | 2025-11-12   | +0.567%    | $46,050.89
3   | 2025-11-13   | -0.234%    | $45,943.12
4   | 2025-11-14   | +2.123%    | $46,918.45
5   | 2025-11-15   | +0.891%    | $47,336.32
6   | 2025-11-16   | -0.456%    | $47,120.51
7   | 2025-11-17   | +1.234%    | $47,702.31

Estadísticas:
- Cambio Promedio: +0.766%
- Cambio Máximo: +2.123%
- Cambio Mínimo: -0.456%
```

**Interpretación:**
- La tendencia general es alcista (+0.766% promedio)
- El día más alcista sería el día 4 (+2.123%)
- Solo hay 2 días bajistas en la semana
- Precio final esperado: $47,702.31 (+5.45% total)

---

### Ejemplo 3: Comparación de Predicciones

**Escenario:** Quieres comparar predicciones a corto, medio y largo plazo.

**Pasos:**
1. Ve al tab "📈 Predicción"
2. Baja hasta "Comparación de Predicciones"
3. Haz clic en "🔄 Generar Comparación Completa"
4. Observa el gráfico con las 3 líneas

**Resultado Esperado:**
```
Gráfico Comparativo:

Línea Verde (1 día):
  Fecha: 2025-11-11
  Precio: $46,234.50

Línea Naranja (5 días):
  Día 1: $46,234.50
  Día 2: $46,789.20
  Día 3: $47,123.45
  Día 4: $47,891.23
  Día 5: $48,234.56

Línea Roja (10 días):
  Día 1: $46,234.50
  Día 5: $48,234.56
  Día 10: $49,876.32
```

**Interpretación:**
- Las 3 predicciones son alcistas
- Las predicciones divergen con el tiempo (mayor incertidumbre)
- La predicción de 10 días es más optimista que la de 1 día
- Esto es normal: las predicciones de largo plazo acumulan cambios

---

## 🎯 Casos de Uso Comunes

### Caso 1: Trading de Corto Plazo

**Objetivo:** Decidir si comprar/vender hoy para mañana.

**Estrategia:**
1. Usa "Predecir Mañana"
2. Si el cambio predicho > +1%: Considera comprar
3. Si el cambio predicho < -1%: Considera vender
4. Si está entre -1% y +1%: Considera mantener

**Ejemplo:**
```python
Predicción: +2.5%
Decisión: COMPRAR (cambio > +1%)

Predicción: -1.8%
Decisión: VENDER (cambio < -1%)

Predicción: +0.3%
Decisión: MANTENER (cambio entre -1% y +1%)
```

---

### Caso 2: Inversión de Medio Plazo

**Objetivo:** Decidir si invertir para la próxima semana.

**Estrategia:**
1. Usa "Predicción Múltiples Días" con 7 días
2. Calcula el cambio total acumulado
3. Revisa las estadísticas
4. Observa la tendencia en el gráfico

**Ejemplo:**
```python
Cambio Acumulado 7 días: +5.5%
Cambio Promedio: +0.786%
Días Alcistas: 5/7
Días Bajistas: 2/7

Decisión: Tendencia alcista clara → Considerar inversión
```

---

### Caso 3: Análisis de Tendencia

**Objetivo:** Entender la tendencia del mercado.

**Estrategia:**
1. Ve al tab "🔍 Exploración de Datos"
2. Selecciona "Últimos 3 Meses"
3. Observa el gráfico de velas
4. Revisa la volatilidad
5. Analiza la distribución de retornos

**Ejemplo:**
```python
Período: Últimos 3 Meses
Precio Inicio: $42,000
Precio Final: $45,234
Cambio: +7.70%

Volatilidad 7 días: 2.3% (Baja)
Volatilidad 30 días: 3.1% (Moderada)

Interpretación: 
- Tendencia alcista clara
- Volatilidad moderada
- Buen momento para inversión de medio plazo
```

---

### Caso 4: Análisis de Riesgo

**Objetivo:** Evaluar el riesgo antes de invertir.

**Estrategia:**
1. Ve al tab "🔍 Exploración de Datos"
2. Revisa el gráfico de volatilidad
3. Observa la distribución de retornos
4. Identifica períodos de alta volatilidad

**Ejemplo:**
```python
Volatilidad Actual: 4.5%
Volatilidad Promedio (30d): 3.2%
Riesgo: ALTO (volatilidad > promedio)

Distribución de Retornos:
- 68% entre -2% y +2%
- 95% entre -4% y +4%
- Máximo observado: +8.5%
- Mínimo observado: -6.2%

Interpretación:
- Mayor riesgo de lo normal
- Posibles movimientos bruscos
- Ajustar posición según tolerancia al riesgo
```

---

## 📊 Interpretación de Resultados

### Predicciones Alcistas (+)

**Cambio Pequeño (+0.1% a +1%)**
```
Interpretación: Ligera tendencia alcista
Confianza: Media
Acción Sugerida: Mantener posiciones actuales
```

**Cambio Moderado (+1% a +3%)**
```
Interpretación: Tendencia alcista clara
Confianza: Alta
Acción Sugerida: Considerar compra
```

**Cambio Grande (+3% o más)**
```
Interpretación: Fuerte tendencia alcista
Confianza: Verificar con otras fuentes
Acción Sugerida: Oportunidad, pero con cautela
```

---

### Predicciones Bajistas (-)

**Cambio Pequeño (-0.1% a -1%)**
```
Interpretación: Ligera tendencia bajista
Confianza: Media
Acción Sugerida: Monitorear de cerca
```

**Cambio Moderado (-1% a -3%)**
```
Interpretación: Tendencia bajista clara
Confianza: Alta
Acción Sugerida: Considerar reducir posición
```

**Cambio Grande (-3% o menos)**
```
Interpretación: Fuerte tendencia bajista
Confianza: Verificar con otras fuentes
Acción Sugerida: Considerar salida
```

---

### Volatilidad

**Baja Volatilidad (< 2%)**
```
Interpretación: Mercado estable
Riesgo: Bajo
Predicciones: Más confiables
```

**Moderada Volatilidad (2% - 4%)**
```
Interpretación: Mercado normal
Riesgo: Moderado
Predicciones: Confiables
```

**Alta Volatilidad (> 4%)**
```
Interpretación: Mercado volátil
Riesgo: Alto
Predicciones: Menos confiables, usar con cautela
```

---

## 🔧 Troubleshooting

### Problema 1: Predicción Muy Diferente de la Realidad

**Síntomas:**
```
Predicción: +5%
Realidad: -3%
Error: 8%
```

**Causas Posibles:**
- Evento extraordinario no capturado (noticias, regulaciones)
- Alta volatilidad del mercado
- Cambio de tendencia
- Modelo necesita reentrenamiento

**Soluciones:**
1. Verifica noticias recientes de Bitcoin
2. Revisa la volatilidad en el tab de exploración
3. Compara predicciones a diferentes plazos
4. Considera factores externos

---

### Problema 2: Predicciones Muy Conservadoras

**Síntomas:**
```
Todas las predicciones entre -0.5% y +0.5%
Realidad: Movimientos de ±3%
```

**Causas Posibles:**
- Modelo entrenado en período de baja volatilidad
- Features no capturan la volatilidad actual
- Necesita reentrenamiento

**Soluciones:**
1. Usa las predicciones como referencia, no como absoluto
2. Combina con otros análisis
3. Considera reentrenar el modelo con datos recientes

---

### Problema 3: Gráficos No Interactivos

**Síntomas:**
- No puedes hacer zoom
- No aparecen tooltips
- Gráficos estáticos

**Soluciones:**
1. Verifica que Plotly esté instalado: `pip list | findstr plotly`
2. Reinstala Plotly: `pip install --upgrade plotly`
3. Actualiza tu navegador
4. Borra caché del navegador

---

### Problema 4: Error al Cargar el Modelo

**Síntomas:**
```
Error: No se encontró el modelo en models/model_feedback.pkl
```

**Soluciones:**
1. Verifica que existe el archivo `models/model_feedback.pkl`
2. Verifica los permisos de lectura
3. Verifica que el modelo sea compatible con la versión de scikit-learn

---

## 🎨 Personalización

### Cambiar Colores de los Gráficos

Edita `config.py`:
```python
COLOR_BULLISH = "#00ff00"  # Verde más brillante
COLOR_BEARISH = "#ff0000"  # Rojo más brillante
COLOR_PREDICTION = "#ff00ff"  # Magenta para predicciones
```

---

### Cambiar Períodos por Defecto

Edita `config.py`:
```python
DEFAULT_N_RECENT_SIMPLE = 500  # Usar 500 registros en vez de 400
DEFAULT_PREDICTION_DAYS = 14   # Predecir 14 días por defecto
```

---

### Añadir Nuevos Filtros Temporales

Edita `config.py`:
```python
FILTER_OPTIONS = [
    "Última Semana",
    "Último Mes",
    "Últimos 2 Meses",  # NUEVO
    "Últimos 3 Meses",
    "Últimos 6 Meses",
    "Último Año",
    "Últimos 2 Años",  # NUEVO
    "Todo"
]

FILTER_DAYS = {
    "Última Semana": 7,
    "Último Mes": 30,
    "Últimos 2 Meses": 60,  # NUEVO
    "Últimos 3 Meses": 90,
    "Últimos 6 Meses": 180,
    "Último Año": 365,
    "Últimos 2 Años": 730,  # NUEVO
    "Todo": None
}
```

---

### Cambiar Métricas Mostradas

Edita `main_mejorado.py` en la sección de métricas:
```python
# Añadir nueva métrica
metric_col4.metric("Volatilidad", f"{volatility:.2f}%")
```

---

## 📈 Mejores Prácticas

### 1. Verificación Cruzada
```python
Paso 1: Hacer predicción con el modelo
Paso 2: Verificar volatilidad reciente
Paso 3: Revisar noticias del mercado
Paso 4: Comparar con otros indicadores técnicos
Paso 5: Tomar decisión informada
```

### 2. Gestión de Riesgo
```python
Nunca inviertas más del X% de tu capital
Usa stop-loss basados en volatilidad
Diversifica tu portafolio
No confíes solo en un modelo
```

### 3. Monitoreo Continuo
```python
Revisa predicciones diariamente
Compara predicción vs realidad
Ajusta estrategia según resultados
Mantente actualizado con noticias
```

---

## 🏆 Casos de Éxito (Ejemplos Hipotéticos)

### Ejemplo 1: Trading Exitoso
```
Fecha: 2025-11-01
Predicción: +2.5%
Precio Inicial: $45,000
Acción: COMPRAR

Fecha: 2025-11-02
Precio Final: $46,125
Cambio Real: +2.5%
Resultado: ✅ Predicción acertada
Ganancia: $1,125 por BTC
```

### Ejemplo 2: Evitar Pérdida
```
Fecha: 2025-11-05
Predicción: -3.2%
Precio Inicial: $47,000
Acción: VENDER

Fecha: 2025-11-06
Precio Final: $45,500
Cambio Real: -3.2%
Resultado: ✅ Pérdida evitada
Ahorro: $1,500 por BTC
```

---

## 📞 Soporte

¿Tienes más preguntas? Consulta:
- `README_MEJORADO.md` - Documentación completa
- `GUIA_RAPIDA.md` - Guía de uso
- Tab "🧠 Sobre el Modelo" - Información técnica

---

**¡Éxito en tus predicciones! 🚀₿**
