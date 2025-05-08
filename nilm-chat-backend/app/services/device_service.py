from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.electrical_data import ElectricalData

def get_cluster_summaries(db: Session):
    # For SQLite: Get most common device_state per cluster using count
    subquery = (
        db.query(
            ElectricalData.cluster,
            ElectricalData.device_state,
            func.count().label("count")
        )
        .group_by(ElectricalData.cluster, ElectricalData.device_state)
        .subquery()
    )

    # For each cluster, pick the device_state with the highest count
    most_common_device_state = (
        db.query(
            subquery.c.cluster,
            subquery.c.device_state
        )
        .order_by(subquery.c.cluster, desc(subquery.c.count))
        .distinct(subquery.c.cluster)
        .all()
    )

    # Map to dictionary for quick lookup
    cluster_to_device = {row.cluster: row.device_state for row in most_common_device_state}

    # Get power and THD averages per cluster
    results = (
        db.query(
            ElectricalData.cluster,
            func.avg(ElectricalData.real_power_watt).label("typical_power"),
            func.avg(ElectricalData.thd).label("typical_thd")
        )
        .group_by(ElectricalData.cluster)
        .all()
    )

    return [
        {
            "id": row.cluster,
            "name": cluster_to_device.get(row.cluster, f"Unknown Device (Cluster {row.cluster})"),
            "cluster": row.cluster,
            "typical_power": row.typical_power,
            "typical_thd": row.typical_thd,
            "description": "Identified device" if cluster_to_device.get(row.cluster) else "Unidentified device"
        }
        for row in results
    ]
