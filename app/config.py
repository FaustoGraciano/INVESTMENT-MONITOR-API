"""
Configuración de la Aplicación
================================

Este módulo centraliza todas las configuraciones de la aplicación
usando variables de entorno con valores por defecto.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuración principal de la aplicación.
    
    Pydantic Settings carga automáticamente valores desde:
    1. Variables de entorno del sistema
    2. Archivo .env (si existe)
    3. Valores por defecto definidos aquí
    """
    
    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",  # Busca este archivo automáticamente
        env_file_encoding="utf-8",
        case_sensitive=False  # API_HOST o api_host funcionan igual
    )
    
    # Información de la aplicación
    app_name: str = Field(default="Investment Monitor API", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=True, alias="DEBUG")
    
    # Configuración del servidor
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


# Instancia global de configuración
# Se carga UNA SOLA VEZ cuando se importa este módulo
settings = Settings()


# Para debugging: imprime la config actual
if __name__ == "__main__":
    print("📋 Configuración actual:")
    print(f"  App: {settings.app_name} v{settings.app_version}")
    print(f"  Host: {settings.api_host}:{settings.api_port}")
    print(f"  Debug: {settings.debug}")
    print(f"  Log Level: {settings.log_level}")
