from pathlib import Path
from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_HOST: str
    # DB_PORT: str
    # DB_NAME: str
    DATABASE_URL: str  # e.g., postgresql+psycopg2://user:password@host:port/dbname

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"  # tells pydantic to load from .env

# single settings instance for whole app
settings = Settings()
