# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

---

## [0.1.0] - Sprint 1 - 2026-02-21

### ✨ Added (Funcionalidades nuevas)

- **API REST con FastAPI**: Implementación del servidor backend utilizando FastAPI
- **Endpoint `/health`**: Health check básico para monitoreo del estado de la API
- **Endpoint `/cotizaciones/{ticker}`**: Consulta de precios en tiempo real de activos financieros
- **Integración con Yahoo Finance**: Uso de `yfinance` para obtener datos de mercado financiero
- **Validación de datos**: Schemas con Pydantic para validación automática de requests/responses
- **Documentación automática**: Swagger UI en `/docs` y ReDoc en `/redoc`

### 🐛 Fixed (Correcciones)

- **Validación de tickers flexible**: Corrección en la detección de ETFs y criptomonedas
  - Problema: Solo funcionaba con acciones (AAPL, TSLA) que tienen campo `currentPrice`
  - Solución: Busca precio en múltiples campos (`currentPrice`, `regularMarketPrice`, `previousClose`, `bid`)
  - Ahora soporta: Acciones, ETFs (SPY, QQQ), Criptomonedas (BTC-USD, ETH-USD)

### 🏗️ Architecture (Estructura técnica)

- **Separación de responsabilidades**: Arquitectura modular con capas:
  - `routes/`: Endpoints HTTP
  - `services/`: Lógica de negocio
  - `schemas/`: Validación de datos (Pydantic)
  - `models/`: Modelos de base de datos (preparado para futuro)
- **Configuración centralizada**: Uso de `pydantic-settings` para manejo de variables de entorno
- **Manejo de errores**: Validación de tickers y respuestas HTTP apropiadas (404, 500)

### 🛠️ Technical Stack

- **Python**: 3.11.9
- **FastAPI**: 0.128.6 - Framework web asíncrono
- **Uvicorn**: 0.27.0 - Servidor ASGI
- **yfinance**: 1.1.0 - API de Yahoo Finance
- **Pydantic**: 2.12.5 - Validación de datos
- **Docker**: Preparado para containerización (próximo sprint)

### 📚 Documentation

- README.md con instrucciones de instalación y uso
- Documentación de código con docstrings
- Swagger UI interactivo para testing de endpoints
- Variables de entorno documentadas en `.env.example`

### 🎯 Funcionalidades probadas

- ✅ Consulta de acciones (AAPL, TSLA, GOOGL)
- ✅ Consulta de ETFs (SPY, QQQ)
- ✅ Consulta de criptomonedas (BTC-USD, ETH-USD)
- ✅ Manejo de errores para tickers inválidos
- ✅ Validación automática de tipos de datos

---

## [Unreleased] - Próximos Sprints

### ✨ Added (Sprint 2 - Persistencia de Datos)

- **Integración con PostgreSQL**: Persistencia real de cotizaciones consultadas.
- **Modelo `Cotizacion` con SQLAlchemy**: Estructura de tabla para almacenar histórico de precios.
- **Migraciones con Alembic**: Versionado de esquema de base de datos.
- **Endpoint `/historico/{ticker}`**: Consulta del historial de cotizaciones para un ticker específico.
- **Schema `HistoricoResponse`**: Respuesta estructurada con `ticker`, `total_registros` y `datos`.

### 🏗️ Architecture (Sprint 2)

- **Servicio de base de datos**: Separación de lógica de persistencia y consulta en `db_service`.
- **Persistencia automática**: Cada consulta de `/cotizaciones/{ticker}` se guarda en PostgreSQL.
- **Consulta histórica ordenada**: Historial devuelto por fecha de consulta descendente (más reciente primero).

### 🐛 Fixed

- **Compatibilidad de yfinance**: Actualización de dependencia para mitigar errores de consulta (429 / invalid crumb).

### 🚧 Planned (Planeado para futuras versiones)

#### Sprint 2 - Persistencia de Datos
- [x] Integración con PostgreSQL
- [x] Modelos de base de datos con SQLAlchemy
- [x] Migraciones con Alembic
- [x] Endpoints para histórico de cotizaciones
- [ ] Cálculo de rendimientos históricos

#### Sprint 3 - Automatización
- [ ] Worker automático para consulta periódica de precios
- [ ] APScheduler para tareas programadas
- [ ] Docker Compose con múltiples contenedores
- [ ] Logs estructurados

#### Sprint 4 - Deployment
- [ ] Despliegue en Render/Railway
- [ ] CI/CD con GitHub Actions
- [ ] Variables de entorno en producción
- [ ] Monitoreo y alertas

#### Features Futuras
- [ ] API de inflación argentina (comparación de rendimientos)
- [ ] Cálculo de rendimiento real vs inflación
- [ ] Endpoints para múltiples tickers simultáneos
- [ ] Cache de consultas frecuentes
- [ ] Rate limiting
- [ ] Autenticación con JWT (opcional)

---

## Formato de Versiones
- **MAJOR** (1.0.0): Cambios incompatibles con versiones anteriores
- **MINOR** (0.1.0): Nuevas funcionalidades compatibles
- **PATCH** (0.0.1): Correcciones de bugs

---
## Tipos de Cambios

- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades obsoletas (se eliminarán pronto)
- **Removed**: Funcionalidades eliminadas
- **Fixed**: Corrección de bugs
- **Security**: Correcciones de seguridad
