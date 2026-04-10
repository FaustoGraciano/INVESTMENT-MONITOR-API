from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

#Definimos como se muestra en dato en respuesta a la consulta de cotizaciones
class CotizacionResponse(BaseModel):
    #Config para que Pydantic pueda convertir objetos SQLAlchemy a este modelo
    model_config = ConfigDict(from_attributes=True)
    
    ticker: str
    nombre: str
    precio_actual:float
    moneda: str
    fecha_consulta: datetime
    

#Definimos como se muestra el historial de cotizaciones en respuesta a la consulta del historial de un ticker
class HistoricoResponse(BaseModel):    
    ticker: str
    total_registros: int
    datos: list[CotizacionResponse]

class RendimientoResponse(BaseModel):
    ticker:str
    fecha_desde:date
    fecha_hasta:date
    precio_inicial:float
    precio_final:float
    rendimiento_pct:float
    total_registros:int  