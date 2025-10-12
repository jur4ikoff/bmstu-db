from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict

# Схемы для первой ЛР

class SCarScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vin_number: str = Field(
        ..., min_length=6, max_length=12, description="VIN-номер автомобиля"
    )
    registration_plate: Optional[str] = Field(
        ..., min_length=6, max_length=12, description="Номер автомобиля"
    )
    brand: str
    model: str
    mileage: int


class SRequestTripWithScore(BaseModel):
    id: int
    passenger_name: str
    driver_name: str
    price: int
    trip_score: int
    driver_score: float

class SDriverTripStats(BaseModel):
    id: int
    name: str
    experience: int
    score: float
    trip_count: int

class SMetadata(BaseModel):
    table_name: str
    column_name: str
    data_type: str
    is_nullable: bool

class STripsDriverPassengerInfo(BaseModel):
    trip_id: int
    driver_name: str
    passenger_name: str
    source_addr: str
    dest_addr: str  
    trip_price: int


class SScoreBeforeAfterRequest(BaseModel):
    before: float | None
    after: float | None