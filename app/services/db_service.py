#Para manejar todas las operaciones de la DB.
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cotizacion import Cotizacion
from sqlalchemy.future import select

from datetime import datetime, date

async def guardar_cotizacion(db: AsyncSession, data: dict) -> Cotizacion:
    """
        Funcion asincrona para guardar una cotizacion en la DB
        
        Args:
            db: Sesion de DB asincrona
            data: Diccionario con datos de la cotizacion
        
        Returns:
            Obejeto cotizacion guardado en la DB    
    """
    #Creo instancia del modelo
    nueva_cotizacion = Cotizacion(
        ticker= data['ticker'],
        nombre= data['nombre'],
        precio_actual= data['precio_actual'],
        moneda= data['moneda'],
        fecha_consulta= data['fecha_consulta']
    )
    
    #Agregamos cotizacion a la sesion
    db.add(nueva_cotizacion)
    
    #Con await el servidor hace otras tareas mientras se guarda en DB, necesitamos funcion y objetos async
    #Guardamos datos en DB.
    await db.commit()
    
    #Refrescamos para obtener el ID generado para ese nuevo elemento de DB
    await db.refresh(nueva_cotizacion)
    
    #Devolvemos nueva cotizacion para no buscarla en la DB.
    return nueva_cotizacion

async def obtener_historial_db(ticker: str, db: AsyncSession, limite: int = 100) -> list:
    """
    Funcion asincrona para obtener el historial de cotizaciones de un ticker desde la DB, ordenado por fecha de consulta descendente (mas reciente primero). Generando un limite de resultados para evitar sobrecargar la respuesta. 
    
    Args:
        ticker: Simbolo del activo (ej: AAPL, TSLA, SPY, BTC-USD)
        db: Sesion de DB asincrona
        limite: Numero maximo de registros a obtener
    Returns:
        Lista de objetos Cotizacion con el historial de ese ticker
        
    """
    #Realizo query para DB
    query= select(Cotizacion).where(Cotizacion.ticker == ticker.upper()).order_by(Cotizacion.fecha_consulta.desc()).limit(limite)
    
    #Obtenemos resultados como lista de objetos Cotizacion (scalars() convierte a lista de objetos metadata de sql alchemy)
    result= await db.execute(query)
    
    #devolvemos lista con todos los objetos encontrados
    lista= result.scalars().all()
    
    return lista
    
    
async def obtener_cotizaciones_intervalo_db(ticker:str, fecha_desde: date, fecha_hasta:date, db: AsyncSession) -> list:
    """
    Obtiene cotizaciones de un ticker dentro de un intervalo [fecha_desde, fecha_hasta],
    ordenadas de la mas antigua a la mas reciente. 
    
    Args:
        ticker: Simbolo del activo (ej: AAPL, TSLA, SPY, BTC-USD)
        fecha_desde: Fecha inicial del intervalo (formato 'YYYY-MM-DD')
        fecha_hasta: Fecha final del intervalo (formato 'YYYY-MM-DD')
        db: Sesion de DB asincrona
    Returns:
        Lista de objetos Cotizacion dentro del intervalo especificado"""
    
    #Realizo query para DB con filtro por ticker y rango de fechas, ordenado por fecha de consulta ascendente (mas antigua primero)
    query= select(Cotizacion).where(
        Cotizacion.ticker == ticker.upper(),
        Cotizacion.fecha_consulta >= fecha_desde, 
        Cotizacion.fecha_consulta <= fecha_hasta
        ).order_by(Cotizacion.fecha_consulta.asc())
    
    result= await db.execute(query)
    
    #devolvemos lista con todos los objetos encontrados
    return result.scalars().all()    