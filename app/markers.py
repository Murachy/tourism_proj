import os
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import schemas, models
from typing import List

router = APIRouter()
UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/markers/", response_model=schemas.MarkerResponse)
async def create_marker(
    latitude: float = Form(...),
    longitude: float = Form(...),
    comment: str = Form(None),
    photos: List[UploadFile] = [],
    db: Session = Depends(get_db)
):
    marker = models.Marker(latitude=latitude, longitude=longitude, comment=comment)
    db.add(marker)
    db.commit()
    db.refresh(marker)

    for photo in photos:
        filename = f"{marker.id}_{photo.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(await photo.read())
        db_photo = models.Photo(filename=filename, marker_id=marker.id)
        db.add(db_photo)
    db.commit()
    db.refresh(marker)
    return marker

@router.get("/markers/", response_model=List[schemas.MarkerResponse])
def get_markers(db: Session = Depends(get_db)):
    return db.query(models.Marker).all()

@router.delete("/markers/{marker_id}")
def delete_marker(marker_id: int, db: Session = Depends(get_db)):
    marker = db.query(models.Marker).filter(models.Marker.id == marker_id).first()
    if not marker:
        raise HTTPException(status_code=404, detail="Маркер не найден")
    for photo in marker.photos:
        try:
            os.remove(os.path.join(UPLOAD_DIR, photo.filename))
        except FileNotFoundError:
            pass
    db.delete(marker)
    db.commit()
    return {"detail": "Маркер удалён"}
