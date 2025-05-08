from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.electrical_data import ElectricalData

router = APIRouter()

@router.get("/")
def get_sample_data(limit: int = 5, db: Session = Depends(get_db)):
    data = db.query(ElectricalData).limit(limit).all()
    return data
