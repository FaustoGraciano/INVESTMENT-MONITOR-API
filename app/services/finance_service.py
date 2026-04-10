#Se implementara la logica del endpoint
#Separamos la logica del endpoint por un posible cambio de API financiera en futuro.

import yfinance as yf
from datetime import datetime, timedelta, date

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
    
def obtener_precios_periodo(ticker:str, fecha_desde: date, fecha_hasta: date):
    
    """
    Obtiene precio inicial y final desde Yahoo Finance para un intervalo.
    Usa el primer y ultimo cierre disponible en el rango.   
    Args:
        ticker: Símbolo del activo (ej: "AAPL", "SPY", "BTC-USD")
        fecha_desde: Fecha de inicio del intervalo
        fecha_hasta: Fecha de fin del intervalo    
    Returns:    
        tupla con precio inicial y precio final
    """
    data= yf.Ticker(ticker)
    
    #Obtenemos el historial de precios para el intervalo dado (ajustamos fechas para incluir el dia final)
    historial= data.history(start= fecha_desde, end= (fecha_hasta + timedelta(days=1)))
    
    if historial.empty:
        raise ValueError(f"No se encontraron datos para el ticker '{ticker}' en el intervalo dado")
    
    #Obtenemos precio inicial y final del intervalo (primer y ultimo cierre disponible)
    precio_inicial= float(historial['Close'].iloc[0])
    precio_final= float(historial['Close'].iloc[-1])
    
    if precio_inicial <= 0 or precio_final <= 0:
        raise ValueError(f"Datos de precio inválidos para el ticker '{ticker}' en el intervalo dado")
    
    return precio_inicial, precio_final

def calcular_rendimiento(precio_inicial: float, precio_final: float) -> float:
    """"
    Calcula el rendimiento porcentual entre dos precios.
    
    Args:
        precio_inicial: Precio al inicio del periodo
        precio_final: Precio al final del periodo
        
    Returns:
        Rendimiento porcentual
    """
    if precio_inicial <= 0 or precio_final <= 0:
        raise ValueError(f"Datos de precio inválidos para el ticker en el intervalo dado")
    
    rendimiento= ((precio_final - precio_inicial) / precio_inicial) * 100
    
    return rendimiento
    
    