from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from datetime import date

from database.database import Base


class Trip(Base):
    # __tablename__ = "trip"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(Integer, ForeignKey("driver.id"))
    passenger_id: Mapped[int] = mapped_column(Integer, ForeignKey("passenger.id"))
    payment_id: Mapped[int]
    source_address: Mapped[str]
    destenation_address: Mapped[str] 
    price: Mapped[int]
    score: Mapped[int]

    driver: Mapped["Driver"] = relationship()
    passenger: Mapped["Passenger"] = relationship()



class Driver(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int]
    first_name: Mapped[str]
    last_name: Mapped[str]
    experience: Mapped[int]
    score: Mapped[int]
    date_of_birthday: Mapped[date]
    address: Mapped[str]
    document_number: Mapped[int]


class Passenger(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birthday: Mapped[date]
    address: Mapped[str]