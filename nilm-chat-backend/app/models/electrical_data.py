from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ElectricalData(Base):
    __tablename__ = "electrical_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=func.now())
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    real_power = Column(Float, nullable=False)
    reactive_power = Column(Float, nullable=False)
    apparent_power = Column(Float, nullable=False)
    power_factor = Column(Float, nullable=False)
    frequency = Column(Float)
    thd = Column(Float, nullable=False)
    real_power_watt = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=False)