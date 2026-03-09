from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession 
from sqlalchemy.orm import sessionmaker, declarative_base

#URL de conexion a PostgreSQL
#Formato: postgresql+asyncpg://usuario:password@host:puerto/nombre_db
DATABASE_URL = "postgresql+asyncpg://investment_user:dev_password_123@localhost:5432/investment_db"


# Motor async de SQLAlchemy, muestra con echo=true las consultas SQL en consola para debug.
engine = create_async_engine(DATABASE_URL, echo=True)

#Fábrica de sesiones asíncronas para manejar conexiones a la base de datos
async_session_maker = sessionmaker(
    engine,
    #Sesiones asíncronas (no bloqueantes)
    class_=AsyncSession,
    #No borra objetos de mem despues de commit a DB.
    expire_on_commit=False
)

#Clase base para modelos SQLAlchemy
Base= declarative_base()

# Dependency para FastAPI: obtiene una sesión de DB
#Cada endpoint que necesite la DB va a "pedir" una sesión
#Crea una sesion nueva, se la pasa al endpoint y luego cierra automaticamente.
async def get_db():
    async with async_session_maker() as session:
        yield session #Devuelve, espera y cierra sesion al terminar.
        
        


