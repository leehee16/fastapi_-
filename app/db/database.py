from abc import ABC, abstractmethod
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..config import settings
import logging

class DatabaseConnection(ABC):
    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def get_base(self):
        pass

class SQLAlchemyConnection(DatabaseConnection):
    def __init__(self, db_url):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_base(self):
        return self.Base

db_connection = SQLAlchemyConnection(settings.DATABASE_URL)

def get_db():
    return next(db_connection.get_session())

Base = db_connection.get_base()

# 데이터베이스 연결 테스트
def test_db_connection():
    try:
        db = next(db_connection.get_session())
        db.execute(text("SELECT 1"))
        logging.info("Database connection successful")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
    finally:
        db.close()

# 애플리케이션 시작 시 데이터베이스 연결 테스트
test_db_connection()
