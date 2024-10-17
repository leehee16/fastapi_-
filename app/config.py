from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # 루트 디렉토리의 test.db 파일 사용
    PROJECT_NAME: str = "FastAPI Example"
    VERSION: str = "0.1.0"

settings = Settings()
