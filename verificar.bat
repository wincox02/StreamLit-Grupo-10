@echo off
echo ========================================
echo Verificacion de Instalacion
echo ========================================
echo.
echo Verificando dependencias instaladas...
echo.

echo Verificando Streamlit...
python -c "import streamlit; print('  [OK] Streamlit version:', streamlit.__version__)" 2>nul || echo   [ERROR] Streamlit no instalado

echo Verificando Pandas...
python -c "import pandas; print('  [OK] Pandas version:', pandas.__version__)" 2>nul || echo   [ERROR] Pandas no instalado

echo Verificando NumPy...
python -c "import numpy; print('  [OK] NumPy version:', numpy.__version__)" 2>nul || echo   [ERROR] NumPy no instalado

echo Verificando Plotly...
python -c "import plotly; print('  [OK] Plotly version:', plotly.__version__)" 2>nul || echo   [ERROR] Plotly no instalado

echo Verificando Scikit-learn...
python -c "import sklearn; print('  [OK] Scikit-learn version:', sklearn.__version__)" 2>nul || echo   [ERROR] Scikit-learn no instalado

echo Verificando Joblib...
python -c "import joblib; print('  [OK] Joblib version:', joblib.__version__)" 2>nul || echo   [ERROR] Joblib no instalado

echo.
echo ========================================
echo Verificando archivos del proyecto...
echo ========================================
echo.

if exist main_mejorado.py (
    echo   [OK] main_mejorado.py encontrado
) else (
    echo   [ERROR] main_mejorado.py no encontrado
)

if exist requirements.txt (
    echo   [OK] requirements.txt encontrado
) else (
    echo   [ERROR] requirements.txt no encontrado
)

if exist models\model_feedback.pkl (
    echo   [OK] Modelo encontrado
) else (
    echo   [ADVERTENCIA] Modelo no encontrado - La app podria fallar
)

if exist BTCUSDT_1d_last_year.csv (
    echo   [OK] Archivo de datos encontrado
) else (
    echo   [ADVERTENCIA] Archivo de datos no encontrado - La app podria usar otro archivo
)

echo.
echo ========================================
echo Verificacion completada!
echo ========================================
echo.
echo Si todo esta [OK], puedes ejecutar la app con:
echo   ejecutar.bat
echo.
pause
