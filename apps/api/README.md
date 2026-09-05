# Analytics API

FastAPI ingestion engine and aggregation service for timeseries web analytics, backed by TimescaleDB.

## Features
- Fast event ingestion via `/api/events/`
- Asynchronous IP geolocation lookups
- Rate limiting with SlowAPI
- Timeseries time-bucket aggregations powered by TimescaleDB hyperfunctions
- Lightweight client tracking script served at `/static/analytics.js`
