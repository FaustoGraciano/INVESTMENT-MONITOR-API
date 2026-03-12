from fastapi import APIRouter, HTTPException
#Importamos modelo de respuesta que FastAPI valida
from app.schemas.cotizaciones import CotizacionResponse
#Importamos función para obtener cotización      
from app.services.finance_service import obtener_cotizacion

#Importo funciones para guardar cotizacion en DB.
from app.services.db_service import guardar_cotizacion
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

#Importo funciones para obtener historial de cotizaciones desde DB
from app.services.db_service import obtener_historial_db
from app.schemas.cotizaciones import HistoricoResponse

#Para agrupar endpoints relacionados
router = APIRouter()

# Endpoint para obtener cotización de un activo financiero por su ticker
@router.get("/cotizaciones/{ticker}", response_model=CotizacionResponse)
async def get_cotizaciones(ticker: str, db: AsyncSession = Depends(get_db)):
    
    """
    Obtiene la cotización actual de un activo financiero y la guarda en DB.
    
    Args:
        ticker: Símbolo del activo (ej: AAPL, TSLA, SPY, BTC-USD)
        db: Sesión de base de datos (inyectada automáticamente)
        
    Returns:
        Datos de cotización con precio actual, moneda y timestamp
    """ 
    try:
        data = obtener_cotizacion(ticker)
        await guardar_cotizacion(db , data)
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
        
        
                
"""#endpoint temporal para probar conexion con DB        
@router.get("/cotizaciones/test/{ticker}")
async def test_guardar(ticker: str, db: AsyncSession = Depends(get_db)):
    #Endpoint de prueba para guardar sin llamar a Yahoo Finance
    from datetime import datetime
    
    # Datos simulados
    data = {
        "ticker": ticker.upper(),
        "nombre": f"Test {ticker.upper()} Inc.",
        "precio_actual": 123.45,
        "moneda": "USD",
        "fecha_consulta": datetime.now()
    }
    
    # Guardar en DB
    await guardar_cotizacion(db, data)
    
    return data
"""

@router.get("/historico/{ticker}", response_model= HistoricoResponse )
async def get_historico(ticker: str, db: AsyncSession = Depends(get_db)):
    
    data= await obtener_historial_db(ticker,db)
    
    return HistoricoResponse(
        ticker= ticker.upper(),
        total_registros= len(data),
        datos= data
    )
    