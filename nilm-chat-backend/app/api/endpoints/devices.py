from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.device_service import get_cluster_summaries

router = APIRouter()

@router.get("/")
def fetch_devices(db: Session = Depends(get_db)):
    try:
        return get_cluster_summaries(db)
    except Exception as e:
        return {"detail": f"Failed to fetch devices: {str(e)}"}
