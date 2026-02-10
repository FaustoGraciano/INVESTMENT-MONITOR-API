from fastapi import APIRouter, HTTPException
#Importamos modelo de respuesta que FastAPI valida
from app.schemas.cotizaciones import CotizacionResponse
#Importamos función para obtener cotización      
from app.services.finance_service import obtener_cotizacion

#Para agrupar endpoints relacionados
router = APIRouter()

# Endpoint para obtener cotización de un activo financiero por su ticker
@router.get("/cotizaciones/{ticker}", response_model=CotizacionResponse)
def get_cotizaciones(ticker: str):
    try:
        data = obtener_cotizacion(ticker)
        return data
    except ValueError as e:
        # Error específico cuando el ticker no existe
        raise HTTPException(
            status_code=404, 
            detail=f"Ticker '{ticker.upper()}' no encontrado. Verificá que sea válido."
        )
    except Exception as e:
        # Cualquier otro error inesperado como yfinance caído o problemas de red
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener cotización: {str(e)}"
        )