import datetime
from _decimal import Decimal

from sqlalchemy import String, Integer
from sqlalchemy.dialects.mssql import DATETIME2, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped

from data_access.entities import Base


class GetPoliciesByVehicleModel(Base):
    __table_args__ = {'schema': 'dbo'}
    __tablename__ = 'fntGetPoliciesByVehicle'

    # Database structure
    PolicyId: Mapped[int] = mapped_column(Integer(), primary_key=True)
    Risk: Mapped[str] = mapped_column(String(128))
    Currency: Mapped[str] = mapped_column(String(128))
    StartDate: Mapped[datetime.date] = mapped_column(DATETIME2)
    EndDate: Mapped[datetime.date] = mapped_column(DATETIME2)
    Premium: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=2))
    Name: Mapped[str] = mapped_column(String(128))
    LastName: Mapped[str] = mapped_column(String(128))
    Pesel: Mapped[str] = mapped_column(String(11))
    Broker: Mapped[str] = mapped_column(String(128))
    InsurerName: Mapped[str] = mapped_column(String(128))
