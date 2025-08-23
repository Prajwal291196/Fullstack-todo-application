from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

class Config:
    env_file = ".env"   # tells pydantic to load from .env

# single settings instance for whole app
settings = Settings()
