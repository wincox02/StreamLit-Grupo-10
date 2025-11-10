@echo off
echo ========================================
echo Bitcoin Price Predictor - Setup
echo ========================================
echo.
echo Instalando dependencias...
echo.

pip install streamlit pandas numpy scikit-learn plotly joblib

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion mejorada:
echo   streamlit run main_mejorado.py
echo.
echo Para ejecutar la aplicacion original:
echo   streamlit run main.py
echo.
pause
