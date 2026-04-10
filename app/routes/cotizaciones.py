from fastapi import APIRouter, HTTPException, Depends
#Importamos modelo de respuesta que FastAPI valida
from app.schemas.cotizaciones import CotizacionResponse, RendimientoResponse, HistoricoResponse
#Importamos función para obtener cotización      
from app.services.finance_service import obtener_cotizacion, calcular_rendimiento, obtener_precios_periodo

#Importo funciones para guardar cotizacion en DB.
from app.services.db_service import guardar_cotizacion, obtener_historial_db, obtener_cotizaciones_intervalo_db
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, date


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


@router.get("/rendimiento/{ticker}", response_model = RendimientoResponse)
async def get_rendimiento(ticker: str, fecha_desde:date, fecha_hasta: date, db: AsyncSession = Depends(get_db)):
    
    if (fecha_desde > fecha_hasta):
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser anterior a la fecha de fin."
        )

    # Convertimos a limites datetime para incluir todo el rango de dias en la consulta SQL.
    fecha_desde_dt = datetime.combine(fecha_desde, datetime.min.time())
    fecha_hasta_dt = datetime.combine(fecha_hasta, datetime.max.time())
    
    try:
        #Obtenemos cotizaciones del intervalo solicitado desde la DB, ordenadas por fecha ascendente (mas antigua primero)
        registros= await obtener_cotizaciones_intervalo_db(ticker, fecha_desde_dt, fecha_hasta_dt, db)
        tot_registros=len(registros)
        
        if tot_registros >= 2:
            precio_inicial= registros[0].precio_actual
            precio_final= registros[-1].precio_actual
        else:
            precio_inicial, precio_final = obtener_precios_periodo(ticker, fecha_desde, fecha_hasta)

        rendimiento= calcular_rendimiento(precio_inicial, precio_final)
        
        return RendimientoResponse(
            ticker= ticker.upper(),
            fecha_desde= fecha_desde,
            fecha_hasta= fecha_hasta,
            precio_inicial= precio_inicial,
            precio_final= precio_final,
            rendimiento_pct= rendimiento,
            total_registros= tot_registros)
    
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular rendimiento: {str(e)}"
        )    