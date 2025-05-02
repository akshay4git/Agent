from typing import Dict, List, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.electrical_data import ElectricalData

def get_cluster_device_mapping() -> Dict[int, Dict[str, str]]:
    """
    Returns a mapping of cluster IDs to device information
    This is a simplified implementation - in a production system,
    this would be stored in the database
    """
    return {
        0: {
            "name": "Background Power",
            "description": "Always-on devices and standby power consumption"
        },
        1: {
            "name": "Refrigerator",
            "description": "Cooling appliance with periodic cycling behavior"
        },
        2: {
            "name": "Lighting",
            "description": "Combination of different lighting fixtures"
        },
        3: {
            "name": "Electronics",
            "description": "TVs, computers, and other electronic devices"
        },
        4: {
            "name": "Kitchen Appliances",
            "description": "Toasters, microwaves, and other small kitchen devices"
        },
        5: {
            "name": "HVAC",
            "description": "Heating, ventilation, and air conditioning systems"
        },
        6: {
            "name": "Water Heating",
            "description": "Electric water heaters and boilers"
        },
        7: {
            "name": "Large Appliances",
            "description": "Washing machines, dryers, and dishwashers"
        }
    }

async def get_recent_metrics_summary() -> Dict[str, Any]:
    """Get a summary of recent electrical metrics for context in LLM prompts"""
    db = SessionLocal()
    try:
        # Get latest timestamp
        latest_timestamp = db.query(func.max(ElectricalData.timestamp)).scalar()
        
        if not latest_timestamp:
            return {
                "devices": [],
                "total_power": 0,
                "last_updated": str(datetime.now())
            }
        
        # Get recent data within the last minute
        time_window = latest_timestamp - timedelta(minutes=1)
        
        # Get average metrics per cluster
        cluster_metrics = {}
        clusters = db.query(ElectricalData.cluster).distinct().all()
        cluster_ids = [c[0] for c in clusters]
        
        cluster_mapping = get_cluster_device_mapping()
        
        devices = []
        total_power = 0
        
        for cluster_id in cluster_ids:
            # Get the most recent data for this cluster
            recent_data = db.query(
                func.avg(ElectricalData.real_power_watt).label("avg_power"),
                func.avg(ElectricalData.thd).label("avg_thd"),
                func.avg(ElectricalData.power_factor).label("avg_pf")
            ).filter(
                ElectricalData.cluster == cluster_id,
                ElectricalData.timestamp >= time_window
            ).first()
            
            if recent_data.avg_power:
                device_info = cluster_mapping.get(cluster_id, {
                    "name": f"Unknown Device (Cluster {cluster_id})",
                    "description": "Unidentified electrical device"
                })
                
                device = {
                    "name": device_info["name"],
                    "power": round(recent_data.avg_power, 2),
                    "thd": round(recent_data.avg_thd, 2),
                    "power_factor": round(recent_data.avg_pf, 2)
                }
                
                devices.append(device)
                total_power += device["power"]
        
        # Sort devices by power consumption (descending)
        devices.sort(key=lambda x: x["power"], reverse=True)
        
        return {
            "devices": devices,
            "total_power": round(total_power, 2),
            "last_updated": str(latest_timestamp)
        }
    finally:
        db.close()