from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/face-reading")
async def face_reading(request: Request):
    return templates.TemplateResponse("face_reading.html", {"request": request})