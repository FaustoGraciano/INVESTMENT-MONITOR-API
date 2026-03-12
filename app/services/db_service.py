#Para manejar todas las operaciones de la DB.
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cotizacion import Cotizacion
from sqlalchemy.future import select

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
    
    
     