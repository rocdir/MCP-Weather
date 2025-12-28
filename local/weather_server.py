import logging
import httpx
from typing import Any, Optional
from mcp.server.fastmcp import FastMCP

# Configurar logging para que escriba en stderr
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_server")

# Inicializar el servidor FastMCP
mcp = FastMCP("WeatherServer")

# URLs de las APIs
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

@mcp.tool()
async def geocode_city(city_name: str) -> str:
    """
    Convierte el nombre de una ciudad en coordenadas de latitud y longitud.
    
    Args:
        city_name: El nombre de la ciudad a buscar.
    """
    logger.info(f"Geocodificando ciudad: {city_name}")
    params = {
        "name": city_name,
        "count": 1,
        "language": "es",
        "format": "json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(GEOCODING_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return f"No se encontraron resultados para la ciudad: {city_name}"
            
            result = data["results"][0]
            name = result.get("name")
            country = result.get("country")
            lat = result.get("latitude")
            lon = result.get("longitude")
            
            return f"Ciudad: {name}, País: {country}\nLatitud: {lat}, Longitud: {lon}"
        except Exception as e:
            logger.error(f"Error en geocodificación: {e}")
            return f"Error al buscar la ciudad: {str(e)}"

@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """
    Obtiene las condiciones climáticas actuales para una ubicación específica.
    
    Args:
        latitude: Latitud de la ubicación.
        longitude: Longitud de la ubicación.
    """
    logger.info(f"Obteniendo clima actual para: {latitude}, {longitude}")
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current_weather")
            if not current:
                return "No se pudieron obtener los datos climáticos actuales."
            
            temp = current.get("temperature")
            windspeed = current.get("windspeed")
            time = current.get("time")
            
            return (f"Clima actual en ({latitude}, {longitude}):\n"
                    f"- Temperatura: {temp}°C\n"
                    f"- Velocidad del viento: {windspeed} km/h\n"
                    f"- Hora de observación: {time}")
        except Exception as e:
            logger.error(f"Error al obtener clima: {e}")
            return f"Error al obtener el clima: {str(e)}"

@mcp.tool()
async def get_forecast(latitude: float, longitude: float, days: int = 3) -> str:
    """
    Obtiene el pronóstico del tiempo para los próximos días.
    
    Args:
        latitude: Latitud de la ubicación.
        longitude: Longitud de la ubicación.
        days: Número de días de pronóstico (máximo 7).
    """
    logger.info(f"Obteniendo pronóstico para: {latitude}, {longitude} por {days} días")
    if days > 7:
        days = 7
        
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            daily = data.get("daily")
            if not daily:
                return "No se pudo obtener el pronóstico."
            
            forecast_lines = [f"Pronóstico para ({latitude}, {longitude}) por {days} días:"]
            for i in range(len(daily["time"])):
                date = daily["time"][i]
                tmax = daily["temperature_2m_max"][i]
                tmin = daily["temperature_2m_min"][i]
                precip = daily["precipitation_sum"][i]
                forecast_lines.append(f"- {date}: Máx {tmax}°C, Mín {tmin}°C, Precipitación: {precip}mm")
            
            return "\n".join(forecast_lines)
        except Exception as e:
            logger.error(f"Error al obtener pronóstico: {e}")
            return f"Error al obtener el pronóstico: {str(e)}"

if __name__ == "__main__":
    # Ejecutar el servidor usando el transporte stdio
    mcp.run(transport="stdio")
