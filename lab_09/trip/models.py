from database import Base, int_pk

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


class Trip(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id"), nullable=False)
    passenger_id: Mapped[int] = mapped_column(
        ForeignKey("passenger.id"), nullable=False
    )
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"), nullable=False)
    source_address: Mapped[str] = mapped_column(String(128), nullable=False)
    destenation_address: Mapped[str] = mapped_column(String(128), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    driver: Mapped["Driver"] = relationship(back_populates="trips")
