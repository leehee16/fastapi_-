from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..models.memo import Memo
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/todo")
async def todo(request: Request, db: Session = Depends(get_db)):
    memos = db.query(Memo).order_by(Memo.created_at.desc()).all()
    return templates.TemplateResponse("todo.html", {"request": request, "memos": memos})

@router.post("/add-memo")
async def add_memo(content: str = Form(...), db: Session = Depends(get_db)):
    new_memo = Memo(content=content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return RedirectResponse(url="/todo", status_code=303)

@router.post("/update-memo/{memo_id}")
async def update_memo(memo_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    memo.content = content
    db.commit()
    return RedirectResponse(url="/todo", status_code=303)

@router.post("/delete-memo/{memo_id}")
async def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    db.delete(memo)
    db.commit()
    return RedirectResponse(url="/todo", status_code=303)

@router.get("/get-memos")
async def get_memos(db: Session = Depends(get_db)):
    memos = db.query(Memo).all()
    return {"memos": memos}
