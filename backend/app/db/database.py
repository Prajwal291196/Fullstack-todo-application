from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.settings import settings

# SQLAlchemy 2.0 style base
class Base(DeclarativeBase):
    pass

# # Encode password safely for URLs
# encoded_password = quote_plus(settings.DB_PASSWORD)

# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql://{settings.DB_USER}:{encoded_password}"
#     f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# )

# Engine (psycopg3)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # drops dead connections
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
