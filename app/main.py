from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import index, todo, face_reading
from .db.database import DatabaseConnection, SQLAlchemyConnection, Base
from .models import sales
from .config import settings
from datetime import date
import random
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(index.router)
app.include_router(todo.router)
app.include_router(face_reading.router)

def get_db_connection():
    return SQLAlchemyConnection(settings.DATABASE_URL)

app.dependency_overrides[DatabaseConnection] = get_db_connection
