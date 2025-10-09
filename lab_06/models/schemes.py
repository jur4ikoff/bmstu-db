from datetime import datetime, date
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict


class SelectCarScheme(BaseModel):
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


class SelectRequestTripWithScore(BaseModel):
    id: int
    passenger_name: str
    driver_name: str
    price: int
    trip_score: int
    driver_score: float