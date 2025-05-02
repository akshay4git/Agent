from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

# Electrical Data Schemas
class ElectricalDataBase(BaseModel):
    voltage: float
    current: float
    real_power: float
    reactive_power: float
    apparent_power: float
    power_factor: float
    frequency: Optional[float] = None
    thd: float
    real_power_watt: float
    cluster: int

class ElectricalDataCreate(ElectricalDataBase):
    timestamp: datetime = Field(default_factory=datetime.now)

class ElectricalDataResponse(ElectricalDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    session_id: str

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str

# Device Schemas
class DeviceInfo(BaseModel):
    id: int
    name: str = "Unknown Device"
    cluster: int
    typical_power: float
    typical_thd: float
    description: str

# Metrics Schemas
class MetricsSummary(BaseModel):
    total_devices: int
    total_power: float
    avg_power_factor: float
    avg_thd: float
    timestamp: datetime