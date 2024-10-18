from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ..models.sales import Sales
import logging

def get_monthly_sales(db: Session, year: int):
    query = db.query(
        func.strftime('%m', Sales.date).label('month'),
        func.sum(Sales.amount).label('total_amount'),
        func.count(Sales.id).label('sale_count')
    ).filter(func.strftime('%Y', Sales.date) == str(year))\
     .group_by(func.strftime('%m', Sales.date))\
     .order_by(func.strftime('%m', Sales.date))
    
    result = query.all()
    logging.info(f"SQL Query: {query}")
    logging.info(f"Query result: {result}")
    return result

def get_daily_sales(db: Session, year: int, month: int):
    query = db.query(
        func.strftime('%d', Sales.date).label('day'),
        func.sum(Sales.amount).label('total_amount'),
        func.count(Sales.id).label('sale_count')
    ).filter(func.strftime('%Y', Sales.date) == str(year))\
     .filter(func.strftime('%m', Sales.date) == f"{month:02d}")\
     .group_by(func.strftime('%d', Sales.date))\
     .order_by(func.strftime('%d', Sales.date))
    
    result = query.all()
    logging.info(f"SQL Query: {query}")
    logging.info(f"Query result: {result}")
    return result