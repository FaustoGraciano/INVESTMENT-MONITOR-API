#Se implementara la logica del endpoint
#Separamos la logica del endpoint por un posible cambio de API financiera en futuro.

import yfinance as yf
from datetime import datetime

def obtener_cotizacion(ticker: str):
    """
    Obtiene la cotización actual de un ticker desde Yahoo Finance.
    Soporta acciones, ETFs y criptomonedas.
    
    Args:
        ticker: Símbolo del activo (ej: "AAPL", "SPY", "BTC-USD")
        
    Returns:
        dict con datos de la cotización
        
    Raises:
        ValueError: Si el ticker no existe o no tiene datos
    """
    # Descarga info del ticker desde Yahoo Finance
    data = yf.Ticker(ticker)
    info = data.info
    
    # Validación flexible: diferentes activos usan diferentes campos
    precio = (
        info.get("currentPrice") or           # Acciones
        info.get("regularMarketPrice") or     # ETFs, Criptos
        info.get("previousClose") or          # Fallback
        info.get("bid")                       # Último recurso
    )
    
    # Intentamos múltiples campos para el NOMBRE
    nombre = (
        info.get("longName") or               # Acciones (nombre completo)
        info.get("shortName") or              # ETFs, Criptos (nombre corto)
        ticker.upper()                        # Fallback: usar el ticker mismo
    )
    
    # Validación final: si no tiene precio, el ticker es inválido
    if precio is None or precio == 0:
        raise ValueError(f"Ticker '{ticker}' no encontrado o sin datos de precio disponibles")
    
    # Extraemos los datos validados
    return {
        "ticker": ticker.upper(),
        "nombre": nombre,
        "precio_actual": float(precio),  # Aseguramos que sea float
        "moneda": info.get("currency", "USD"),
        "fecha_consulta": datetime.now()
    } 