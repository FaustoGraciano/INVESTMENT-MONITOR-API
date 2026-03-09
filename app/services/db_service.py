#Para manejar todas las operaciones de la DB.
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cotizacion import Cotizacion


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