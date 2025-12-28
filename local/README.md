# Servidor MCP de Clima en Tiempo Real

Este es un servidor que implementa el **Model Context Protocol (MCP)** para proporcionar datos climáticos en tiempo real utilizando la API de [Open-Meteo](https://open-meteo.com/).

## Características

- **Geocodificación**: Busca coordenadas (latitud/longitud) por nombre de ciudad.
- **Clima Actual**: Obtiene temperatura y velocidad del viento actuales.
- **Pronóstico**: Proporciona el pronóstico para los próximos 3 a 7 días.
- **Sin API Key**: Utiliza APIs públicas que no requieren registro.

## Requisitos

- Python 3.10 o superior.
- Dependencias: `mcp`, `httpx`.

## Instalación

1. Clona o descarga los archivos del servidor.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install "mcp[cli]" httpx
   ```

## Uso

Para ejecutar el servidor localmente:
```bash
python weather_server.py
```

### Configuración en Claude Desktop

Para usar este servidor con Claude Desktop, añade la siguiente configuración a tu archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/ruta/a/tu/venv/bin/python",
      "args": ["/ruta/a/tu/weather_server.py"]
    }
  }
}
```

## Herramientas Disponibles

| Herramienta | Descripción |
| :--- | :--- |
| `geocode_city` | Busca las coordenadas de una ciudad por su nombre. |
| `get_current_weather` | Obtiene el clima actual dadas una latitud y longitud. |
| `get_forecast` | Obtiene el pronóstico para los próximos días. |
