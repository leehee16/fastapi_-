from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from ..config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True  # SQL 쿼리 로깅 활성화
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터베이스 연결 테스트
def test_db_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        logging.info("Database connection successful")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
    finally:
        db.close()

# 애플리케이션 시작 시 데이터베이스 연결 테스트
test_db_connection()
