#Se implementara la logica del endpoint
#Separamos la logica del endpoint por un posible cambio de API financiera en futuro.

import yfinance as yf
from datetime import datetime

def obtener_cotizacion(ticker: str):
    #Obtenemos la cotizacion del ticker usando yfinance
    #Descarga info de un ticket especifico
    data= yf.Ticker(ticker)
    info = data.info
    
    # Validación: verificamos que el ticker tenga datos válidos
    precio = info.get("currentPrice")
    nombre = info.get("longName")
    
    # Si no tiene precio O no tiene nombre, el ticker es inválido
    if precio is None or nombre is None:
        raise ValueError(f"Ticker '{ticker}' no encontrado o sin datos disponibles")
    
    # Extraemos los datos validados
    return {
        "ticker": ticker.upper(),
        "nombre": nombre,
        "precio_actual": precio,
        "moneda": info.get("currency", "USD"),
        "fecha_consulta": datetime.now()
    } 