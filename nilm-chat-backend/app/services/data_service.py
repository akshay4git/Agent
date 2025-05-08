from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.electrical_data import ElectricalData

async def get_actual_devices(db, hours: int = 24) -> List[Dict[str, Any]]:
    """Extract ONLY real devices found in the dataset"""
    try:
        time_window = datetime.now() - timedelta(hours=hours)
        
        # Get active clusters with their real device names from dataset
        active_devices = db.query(
            ElectricalData.cluster,
            ElectricalData.device_state,
            func.avg(ElectricalData.real_power_watt).label("avg_power"),
            func.avg(ElectricalData.thd).label("avg_thd")
        ).filter(
            ElectricalData.timestamp >= time_window
        ).group_by(
            ElectricalData.cluster,
            ElectricalData.device_state
        ).all()

        # Build response with ONLY real devices
        devices = []
        for cluster, device_state, avg_power, avg_thd in active_devices:
            devices.append({
                "cluster_id": cluster,
                "name": device_state,  # Use actual device name from dataset
                "avg_power": round(avg_power, 2),
                "avg_thd": round(avg_thd, 2),
                "last_seen": str(time_window)
            })

        return devices

    except Exception as e:
        raise Exception(f"Failed to fetch devices: {str(e)}")