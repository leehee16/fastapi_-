from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import index, todo
from .db.database import engine, SessionLocal, test_db_connection
from .models import sales
from .config import settings
from datetime import date, timedelta
import random
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(index.router)
app.include_router(todo.router)

# 데이터베이스 테이블 생성 및 테스트 데이터 추가
@app.on_event("startup")
async def startup():
    test_db_connection()  # 데이터베이스 연결 테스트
    sales.Base.metadata.create_all(bind=engine)
    
    # 테스트 데이터 추가
    db = SessionLocal()
    try:
        # 기존 데이터 모두 삭제
        db.query(sales.Sales).delete()
        db.commit()
        logging.info("All existing data deleted")

        # 새로운 테스트 데이터 추가
        current_year = date.today().year
        for month in range(1, 13):
            for _ in range(random.randint(15, 30)):  # 각 월마다 15~30개의 데이터 포인트 생성
                sale_date = date(current_year, month, random.randint(1, 28))
                amount = random.uniform(500, 15000)  # 더 넓은 범위의 금액
                db_sale = sales.Sales(date=sale_date, amount=amount)
                db.add(db_sale)
        db.commit()
        new_count = db.query(sales.Sales).count()
        logging.info(f"New test data added to the database. New count: {new_count}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error occurred while adding test data: {e}")
    finally:
        db.close()
