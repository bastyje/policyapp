import datetime

from sqlalchemy import Integer, String
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.entities import Base


class Vehicle(Base):
    __tablename__ = 'Vehicle'
    __table_args__ = {'schema': 'dbo'}

    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    Make: Mapped[str] = mapped_column(String(64))
    Model: Mapped[str] = mapped_column(String(64))
    RegistrationNumber: Mapped[str] = mapped_column(String(16))
    Vin: Mapped[str] = mapped_column(String(17))
    ProductionYear: Mapped[int] = mapped_column(Integer())
    RegistrationDate: Mapped[datetime.date] = mapped_column(DATETIME2())
    OwnerCount: Mapped[int] = mapped_column(Integer())

    Policy: Mapped['Policy'] = relationship(back_populates='Vehicle')
