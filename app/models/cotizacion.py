from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

#Creamos tabla de cotizaciones para DB PostgreSQL usando SQLAlchemy

class Cotizacion(Base):
    __tablename__ = "cotizaciones"
    
    #Columnas de la tabla:      #index=True hace consultas mas rapidas por ese campo.
    id= Column(Integer, primary_key=True, index=True)
    ticker= Column(String, index=True)
    nombre= Column(String)
    precio_actual= Column(Float)
    moneda= Column(String)
    fecha_consulta= Column(DateTime, default= datetime.now)
    
    