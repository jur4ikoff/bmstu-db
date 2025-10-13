from datetime import date
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict


class SDriverScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_id: int
    first_name: str
    last_name: str
    experience: int
    score: float
    date_of_birthday: date
    address: str
    document_number: int


