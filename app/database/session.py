from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

# Get database connection details from environment variables
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'user')}:"
    f"{os.getenv('DB_PASSWORD', 'password')}@"
    f"{os.getenv('DB_HOST', 'localhost')}/"
    f"{os.getenv('DB_NAME', 'mydb')}"
)

# Create engine with connection pooling disabled for better performance in async contexts
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
