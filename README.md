# 📊 Investment Monitor API

Sistema de monitoreo de inversiones que rastrea automáticamente el rendimiento de activos financieros y lo compara contra la inflación argentina.

## 🎯 Objetivo del Proyecto

Backend profesional desarrollado como proyecto portfolio para demostrar habilidades en:
- Desarrollo de APIs REST con FastAPI
- Integración con servicios externos (Yahoo Finance)
- Persistencia de datos con PostgreSQL
- Dockerización y despliegue en la nube
- Buenas prácticas de arquitectura de software

## 🛠️ Stack Tecnológico

- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy** - ORM para manejo de base de datos
- **Docker** - Containerización
- **yfinance** - Integración con Yahoo Finance

## 📁 Estructura del Proyecto

```
app/
├── models/      # Modelos de base de datos (SQLAlchemy)
├── routes/      # Endpoints de la API
├── schemas/     # Validación de datos (Pydantic)
├── services/    # Lógica de negocio
└── config.py    # Configuración de la aplicación
```

## 🚀 Estado del Desarrollo

- [x] Estructura del proyecto
- [x] API básica con FastAPI
- [x] Integración con Yahoo Finance
- [x] Base de datos PostgreSQL
- [x] Dockerización
- [x] Endpoint de histórico por ticker (`/historico/{ticker}`)
- [x] Cálculo de rendimiento simple porcentual por intervalo (`/rendimiento/{ticker}`)
- [ ] Worker automático para consulta periódica de precios
- [ ] APScheduler para tareas programadas
- [ ] Logs estructurados
- [ ] Deploy en producción

## 📌 Endpoints Disponibles

- **GET /health**: Verifica el estado de la API
- **GET /cotizaciones/{ticker}**: Consulta la cotización actual y la persiste en PostgreSQL
- **GET /historico/{ticker}**: Devuelve el historial de cotizaciones guardadas para un ticker
- **GET /rendimiento/{ticker}?fecha_desde=YYYY-MM-DD&fecha_hasta=YYYY-MM-DD**: Calcula rendimiento simple porcentual en el intervalo
	- Usa DB cuando hay suficientes registros históricos
	- Si no hay suficientes registros, usa Yahoo Finance como fallback

## 👨‍💻 Autor

**Fausto Graciano**  
Estudiante de Ingeniería en Computación  
[GitHub](https://github.com/tu-usuario) | [LinkedIn](https://linkedin.com/in/tu-perfil)

---

*Proyecto en desarrollo activo - Marzo 2026*
