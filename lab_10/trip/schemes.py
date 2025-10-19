from pydantic import BaseModel, ConfigDict


class Trip(BaseModel):
    id: int
    driver_id: int
    passenger_id: int
    payment_id: int
    source_address: str
    destenation_address: str
    price: int
    score: int

    model_config = ConfigDict(from_attributes=True)
