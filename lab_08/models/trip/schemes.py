from datetime import datetime, date
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class STripScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_address: str
    destenation_address: str
    price: int
    score: int


class STripFullScheme(BaseModel):
    id: int

    driver_id: int
    driver_name: str 
    driver_score: float

    passenger_id: int
    passenger_name: str
    
    src_address: str
    dest_address: str

    price: int
    score: int


class CrTrip(BaseModel):
    driver_id: int
    passenger_id: int
    payment_id: int
    source_address: str
    destenation_address: str
    price: int
    score: int

class UpdTrip(BaseModel):
    driver_id: Optional[int] = None
    passenger_id: Optional[int] = None
    price: Optional[int] = None
    score: Optional[int] = None