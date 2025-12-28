import logging
import httpx
from typing import Any
from fastmcp import FastMCP

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_server")

# Inicializar el servidor FastMCP
# Nota: No usamos mcp.run() aquí porque Vercel manejará la ejecución de la app ASGI
mcp = FastMCP("WeatherServer")

# URLs de las APIs
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

@mcp.tool()
async def geocode_city(city_name: str) -> str:
    """Convierte el nombre de una ciudad en coordenadas."""
    params = {"name": city_name, "count": 1, "language": "es", "format": "json"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(GEOCODING_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if not data.get("results"):
                return f"No se encontraron resultados para: {city_name}"
            result = data["results"][0]
            return f"Ciudad: {result['name']}, País: {result['country']}\nLatitud: {result['latitude']}, Longitud: {result['longitude']}"
        except Exception as e:
            return f"Error: {str(e)}"

@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """Obtiene el clima actual."""
    params = {"latitude": latitude, "longitude": longitude, "current_weather": "true", "timezone": "auto"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            current = data.get("current_weather")
            if not current: return "No hay datos."
            return f"Clima en ({latitude}, {longitude}): {current['temperature']}°C, Viento: {current['windspeed']} km/h"
        except Exception as e:
            return f"Error: {str(e)}"

# Exportar la aplicación ASGI para Vercel
# FastMCP proporciona un método para obtener la app compatible con Starlette/FastAPI
app = mcp.http_app()
