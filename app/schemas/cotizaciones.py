from pydantic import BaseModel
from datetime import datetime

#Definimos como se muestra en dato en respuesta a la consulta de cotizaciones
class CotizacionResponse(BaseModel):
    ticker: str
    nombre: str
    precio_actual:float
    moneda: str
    fecha_consulta: datetime
    
    