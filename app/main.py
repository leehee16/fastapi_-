from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .routes import index, todo, face_reading
from .db.database import DatabaseConnection, SQLAlchemyConnection, Base
from .models import sales
from .config import settings
from datetime import date
import random
import logging
import os

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(index.router)
app.include_router(todo.router)
app.include_router(face_reading.router)

def get_db_connection():
    return SQLAlchemyConnection(settings.DATABASE_URL)

app.dependency_overrides[DatabaseConnection] = get_db_connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 구체적인 origin을 지정해야 합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
