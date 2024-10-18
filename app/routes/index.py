from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..db.database import DatabaseConnection
from ..crud import sales as sales_crud
from datetime import datetime
import logging
import random
from calendar import monthrange

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def index(request: Request, db_connection: DatabaseConnection = Depends(), selected_month: int = None):
    db = next(db_connection.get_session())
    current_year = datetime.now().year
    
    if selected_month:
        sales_data = sales_crud.get_daily_sales(db, current_year, selected_month)
    else:
        sales_data = sales_crud.get_monthly_sales(db, current_year)
    
    logging.info(f"Current year: {current_year}")
    logging.info(f"Raw sales data: {sales_data}")
    
    if not sales_data:
        logging.warning("No sales data found for the selected period")
        formatted_sales_data = []
    else:
        if selected_month:
            formatted_sales_data = [
                {
                    "date": f"{sale.day}일",
                    "total_amount": round(float(sale.total_amount), 2),
                    "sale_count": sale.sale_count,
                    "average_amount": round(float(sale.total_amount) / sale.sale_count, 2) if sale.sale_count else 0
                } for sale in sales_data
            ]
        else:
            formatted_sales_data = [
                {
                    "month": f"{int(sale.month)}월",
                    "total_amount": round(float(sale.total_amount), 2),
                    "sale_count": sale.sale_count,
                    "average_amount": round(float(sale.total_amount) / sale.sale_count, 2) if sale.sale_count else 0
                } for sale in sales_data
            ]
    
    logging.info(f"Formatted sales data: {formatted_sales_data}")
    
    # 색깔별 판매 수량 데이터 (더 다양한 범위의 랜덤 데이터)
    colors = ["hungry", "black", "pink", "Yellow", "hojin", "ggul", "zzz", "🥹"]
    color_sales = [
        {"color": color, "sales": random.randint(100, 1000)}
        for color in random.sample(colors, 5)  # 랜덤하게 5개의 색상 선택
    ]
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "sales_data": formatted_sales_data,
        "color_sales": color_sales,
        "selected_month": selected_month,
        "months": range(1, 13),
    })
