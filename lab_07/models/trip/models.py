from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from database.database import Base

class Trip(Base):
    # __tablename__ = "trip"

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, nullable=False)
    passenger_id = Column(Integer, nullable=False)
    payment_id = Column(Integer, nullable=False)
    source_address = Column(String, nullable=False)
    destenation_address = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)