from pydantic import BaseModel, ConfigDict
from datetime import date

class Driver(BaseModel):
    id: int
    car_id: int
    first_name: str
    last_name: str
    experience: int
    score: str
    date_of_birthday: date
    address: str | None = None
    document_number: int

    model_config = ConfigDict(from_attributes=True)