from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс настроек — строго из .env"""
    APP_NAME: str
    ENV: str

    JWT_SECRET: str
    JWT_ALG: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    SQLITE_PATH: str 

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

settings = Settings()