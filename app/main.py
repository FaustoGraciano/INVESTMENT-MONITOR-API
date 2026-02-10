
from fastapi import FastAPI
from app.config import settings

# Importamos rutas
from app.routes import cotizaciones

# Creamos instancia de FastAPI
app = FastAPI(title=settings.app_name)

# Agregamos endpoints del router a app principal
app.include_router(cotizaciones.router)
    
@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name, "version":settings.app_version}

