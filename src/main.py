import hashlib
import base64
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

SHORT_HOST = 'http://localhost:8000'

class URLCreate(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_id(url: str):
    hash_object = hashlib.md5(url.encode())
    hash_bytes = hash_object.digest()
    short_id = base64.urlsafe_b64encode(hash_bytes).decode()
    return short_id

@app.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    full_url = str(item.url)
    short_id = generate_short_id(full_url)
    existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not existing:
        new_item = URLItem(short_id=short_id, full_url=full_url)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"short_url": f"{SHORT_HOST}/{short_id}"}
    raise HTTPException(status_code=500, detail="Коротка ссылка уже существует")

@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=url_item.full_url)

@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }

@app.delete("/{short_id}")
def delete_short_url(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    
    db.delete(url_item)
    db.commit()
    return {"detail": "Короткая ссылка успешно удалена"}

