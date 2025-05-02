from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Dict
from app.database import get_db
from app.models.electrical_data import ElectricalData
from app.api.schemas import DeviceInfo
from app.services.data_service import get_cluster_device_mapping

router = APIRouter()

@router.get("/", response_model=List[DeviceInfo])
async def get_all_devices(db: Session = Depends(get_db)):
    """Get information about all detected devices"""
    # Get unique clusters
    clusters = db.query(
        distinct(ElectricalData.cluster)
    ).all()
    
    cluster_ids = [c[0] for c in clusters]
    
    # Get device info for each cluster
    devices = []
    cluster_mapping = get_cluster_device_mapping()
    
    for cluster_id in cluster_ids:
        # Get average metrics for this cluster
        avg_metrics = db.query(
            func.avg(ElectricalData.real_power_watt).label("avg_power"),
            func.avg(ElectricalData.thd).label("avg_thd")
        ).filter(
            ElectricalData.cluster == cluster_id
        ).first()
        
        # Create device info
        device_info = cluster_mapping.get(cluster_id, {
            "name": f"Unknown Device (Cluster {cluster_id})",
            "description": "Unidentified electrical device"
        })
        
        devices.append(DeviceInfo(
            id=len(devices) + 1,
            name=device_info["name"],
            cluster=cluster_id,
            typical_power=avg_metrics.avg_power,
            typical_thd=avg_metrics.avg_thd,
            description=device_info["description"]
        ))
    
    return devices

@router.get("/{device_id}", response_model=DeviceInfo)
async def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    """Get information about a specific device"""
    # This is a simplified implementation
    # In a real app, you'd have a proper devices table
    
    devices = await get_all_devices(db)
    
    for device in devices:
        if device.id == device_id:
            return device
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Device with ID {device_id} not found"
    )