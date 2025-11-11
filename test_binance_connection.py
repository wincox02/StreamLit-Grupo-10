"""
Script para probar la conexión a la API de Binance
"""
import requests
import sys

def test_binance_api():
    """Prueba la conexión a diferentes endpoints de Binance"""
    
    print("🔍 Probando conexión a la API de Binance...\n")
    
    endpoints = [
        "https://api.binance.com/api/v3/ping",
        "https://api1.binance.com/api/v3/ping",
        "https://api2.binance.com/api/v3/ping",
        "https://api3.binance.com/api/v3/ping",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    working_endpoints = []
    
    for endpoint in endpoints:
        try:
            print(f"Probando: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"  ✅ Éxito - Código: {response.status_code}")
                working_endpoints.append(endpoint)
            elif response.status_code == 451:
                print(f"  ❌ Error 451 - Acceso restringido desde tu ubicación")
            else:
                print(f"  ⚠️ Error - Código: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout - El servidor no respondió a tiempo")
        except requests.exceptions.ConnectionError:
            print(f"  🔌 Error de conexión - No se pudo conectar")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    # Resumen
    print("\n" + "="*60)
    if working_endpoints:
        print(f"✅ {len(working_endpoints)} endpoint(s) funcionando correctamente:")
        for ep in working_endpoints:
            print(f"   - {ep}")
        print("\n✨ Puedes usar la API de Binance desde tu ubicación")
    else:
        print("❌ Ningún endpoint de Binance está accesible")
        print("\n🔧 Soluciones sugeridas:")
        print("   1. Usa una VPN para cambiar tu ubicación")
        print("   2. Usa los archivos CSV locales (BTCUSDT_1d_*.csv)")
        print("   3. Descarga datos manualmente desde Binance.com")
        print("   4. Usa la opción '📁 Archivo CSV/Local' en la aplicación")
    print("="*60)
    
    return len(working_endpoints) > 0

if __name__ == "__main__":
    success = test_binance_api()
    sys.exit(0 if success else 1)
