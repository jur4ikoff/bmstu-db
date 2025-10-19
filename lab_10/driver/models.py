from database import Base, int_pk

from sqlalchemy import (
    Column,
    Integer,
    String,
    SmallInteger,
    Numeric,
    Date,
    BigInteger,
    ForeignKey,
)

from typing import List
from sqlalchemy.orm import Mapped, relationship


class Driver(Base):
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer)
    first_name = Column(String(63), nullable=False)
    last_name = Column(String(63), nullable=False)
    experience = Column(SmallInteger, nullable=False)
    score = Column(Numeric, nullable=False)  # в Pydantic у вас str, но в БД — NUMERIC
    date_of_birthday = Column(Date, nullable=False)
    address = Column(String(128))
    document_number = Column(BigInteger, nullable=False, unique=True)

    trips: Mapped[List["Trip"]] = relationship(back_populates="driver")
