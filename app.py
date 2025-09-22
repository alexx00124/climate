from flask import Flask, render_template, request, flash
import requests
import os

# Crear la instancia de Flask
app = Flask(__name__)
app.secret_key = 'universitaria123'  # Necesario para flash messages

# Configuración de la API de OpenWeather
API_KEY = '4e5a37629df91bad9ade13bda4dffce8'  # Reemplaza con tu API key de OpenWeatherMap
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def obtener_datos_clima(ciudad):
    """
    Función para obtener datos del clima desde la API de OpenWeather
    
    Args:
        ciudad (str): Nombre de la ciudad
        
    Returns:
        dict: Datos del clima o None si hay error
    """
    try:
        # Parámetros para la petición a la API
        params = {
            'q': ciudad,
            'appid': API_KEY,
            'units': 'metric',  # Para obtener temperatura en Celsius
            'lang': 'es'        # Para descripción en español
        }
        
        # Hacer la petición HTTP GET a la API
        response = requests.get(BASE_URL, params=params)
        
        # Verificar si la petición fue exitosa
        if response.status_code == 200:
            data = response.json()
            
            # Extraer los datos que necesitamos
            datos_clima = {
                'ciudad': data['name'],
                'pais': data['sys']['country'],
                'temperatura': round(data['main']['temp'], 1),
                'sensacion_termica': round(data['main']['feels_like'], 1),
                'humedad': data['main']['humidity'],
                'velocidad_viento': data['wind']['speed'],
                'descripcion': data['weather'][0]['description'].title(),
                'icono': data['weather'][0]['icon'],
                'presion': data['main']['pressure']
            }
            
            return datos_clima
        
        elif response.status_code == 404:
            return {'error': 'Ciudad no encontrada. Verifica el nombre e intenta de nuevo.'}
        else:
            return {'error': f'Error al consultar el clima: {response.status_code}'}
            
    except requests.exceptions.ConnectionError:
        return {'error': 'Error de conexión. Verifica tu conexión a internet.'}
    except requests.exceptions.Timeout:
        return {'error': 'Tiempo de espera agotado. Intenta de nuevo.'}
    except Exception as e:
        return {'error': f'Error inesperado: {str(e)}'}

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Ruta principal que maneja tanto GET como POST
    GET: Muestra el formulario
    POST: Procesa la búsqueda del clima
    """
    datos_clima = None
    
    if request.method == 'POST':
        # Obtener la ciudad del formulario
        ciudad = request.form.get('ciudad', '').strip()
        
        if not ciudad:
            flash('Por favor ingresa el nombre de una ciudad', 'error')
        else:
            # Obtener datos del clima
            datos_clima = obtener_datos_clima(ciudad)
            
            # Si hay error, mostrar mensaje flash
            if datos_clima and 'error' in datos_clima:
                flash(datos_clima['error'], 'error')
                datos_clima = None
    
    # Renderizar la plantilla con los datos
    return render_template('index.html', datos_clima=datos_clima)

@app.errorhandler(404)
def page_not_found(e):
    """Manejo de error 404"""
    return render_template('index.html', error="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(e):
    """Manejo de error 500"""
    return render_template('index.html', error="Error interno del servidor"), 500

if __name__ == '__main__':
    # Verificar que se haya configurado la API key
    if API_KEY == 'TU_API_KEY_AQUI':
        print("¡IMPORTANTE! Debes reemplazar 'TU_API_KEY_AQUI' con tu API key de OpenWeatherMap")
        print("Registro gratuito en: https://openweathermap.org/api")
    
    # Ejecutar la aplicación en modo debug
    app.run(debug=True, host='0.0.0.0', port=5000)