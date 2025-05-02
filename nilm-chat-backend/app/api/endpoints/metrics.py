from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.electrical_data import ElectricalData
from app.api.schemas import MetricsSummary, ElectricalDataResponse

router = APIRouter()

@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary(db: Session = Depends(get_db)):
    """Get summary of current electrical metrics"""
    # Get latest timestamp
    latest_timestamp = db.query(func.max(ElectricalData.timestamp)).scalar()
    
    if not latest_timestamp:
        return MetricsSummary(
            total_devices=0,
            total_power=0.0,
            avg_power_factor=0.0,
            avg_thd=0.0,
            timestamp=datetime.now()
        )
    
    # Get metrics from around the latest timestamp (within 5 seconds)
    time_window = latest_timestamp - timedelta(seconds=5)
    
    recent_data = db.query(ElectricalData).filter(
        ElectricalData.timestamp >= time_window
    ).all()
    
    # Calculate summary metrics
    unique_clusters = set(data.cluster for data in recent_data)
    total_power = sum(data.real_power_watt for data in recent_data) / len(recent_data) if recent_data else 0
    avg_pf = sum(data.power_factor for data in recent_data) / len(recent_data) if recent_data else 0
    avg_thd = sum(data.thd for data in recent_data) / len(recent_data) if recent_data else 0
    
    return MetricsSummary(
        total_devices=len(unique_clusters),
        total_power=total_power,
        avg_power_factor=avg_pf,
        avg_thd=avg_thd,
        timestamp=latest_timestamp
    )

@router.get("/recent", response_model=List[ElectricalDataResponse])
async def get_recent_metrics(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recent electrical measurements"""
    recent_data = db.query(ElectricalData).order_by(
        ElectricalData.timestamp.desc()
    ).limit(limit).all()
    
    return recent_data

@router.get("/by-cluster/{cluster_id}", response_model=List[ElectricalDataResponse])
async def get_metrics_by_cluster(
    cluster_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recent measurements for a specific cluster/device type"""
    cluster_data = db.query(ElectricalData).filter(
        ElectricalData.cluster == cluster_id
    ).order_by(
        ElectricalData.timestamp.desc()
    ).limit(limit).all()
    
    return cluster_data