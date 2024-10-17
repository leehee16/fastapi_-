from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/todo")
async def todo(request: Request):
    return templates.TemplateResponse("todo.html", {"request": request})