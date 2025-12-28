# MCP Weather Server (Real-time Data)

This repository contains a Model Context Protocol (MCP) server that provides real-time weather data using the [Open-Meteo API](https://open-meteo.com/).

## Project Structure

- **/local**: Contains the version for local use via `stdio` transport. Ideal for Claude Desktop.
- **/vercel**: Contains the version adapted for deployment on Vercel using `SSE` (Server-Sent Events) transport.

## Features

- **Geocoding**: Find coordinates by city name.
- **Current Weather**: Get temperature and wind speed.
- **Forecast**: Get weather forecast for the next few days.
- **No API Key Required**: Uses public APIs.

## Quick Start

### Local Use
1. Go to `local/`
2. Install dependencies: `pip install "mcp[cli]" httpx`
3. Run: `python weather_server.py`

### Vercel Deployment
1. Go to `vercel/`
2. Deploy with Vercel CLI: `vercel --prod`
3. See `VERCEL_DEPLOY.md` for more details.

## License
MIT
