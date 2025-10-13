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
