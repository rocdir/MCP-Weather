# Guía de Despliegue en Vercel (MCP SSE)

Para desplegar tu servidor MCP de clima en Vercel, sigue estos pasos. Hemos adaptado el servidor para usar **SSE (Server-Sent Events)**, que es el estándar para servidores MCP alojados en la web.

## Estructura del Proyecto

Asegúrate de tener la siguiente estructura de archivos:
- `api/index.py`: El código del servidor adaptado.
- `vercel.json`: Configuración de rutas para Vercel.
- `requirements.txt`: Dependencias necesarias.

## Pasos para el Despliegue

1. **Instalar Vercel CLI** (si no lo tienes):
   ```bash
   npm i -g vercel
   ```

2. **Login en Vercel**:
   ```bash
   vercel login
   ```

3. **Desplegar**:
   Desde la raíz de tu proyecto (`vercel_mcp/`), ejecuta:
   ```bash
   vercel --prod
   ```

## Configuración en Claude Desktop

Una vez desplegado, obtendrás una URL (ej. `https://tu-proyecto.vercel.app`). Para usarlo en Claude, añade esto a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather-vercel": {
      "url": "https://tu-proyecto.vercel.app/mcp"
    }
  }
}
```

> **Nota**: El endpoint configurado en el código es `/mcp`. Claude se conectará a este endpoint mediante HTTP/SSE.

## Consideraciones Técnicas
- **Stateless**: Vercel Functions son sin estado. El servidor está configurado para manejar peticiones HTTP de forma independiente.
- **Timeout**: Hemos configurado un timeout de 30s para las peticiones a la API de clima para evitar que la función de Vercel termine prematuramente.
