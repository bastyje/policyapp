import datetime
from _decimal import Decimal

from sqlalchemy import String, Integer
from sqlalchemy.dialects.mssql import DATETIME2, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped

from data_access.entities import Base


class GetPoliciesByPersonModel(Base):
    __table_args__ = {'schema': 'dbo'}
    __tablename__ = 'fntGetPoliciesByPerson'

    # Database structure
    PolicyId: Mapped[int] = mapped_column(Integer(), primary_key=True)
    Risk: Mapped[str] = mapped_column(String(128))
    Currency: Mapped[str] = mapped_column(String(128))
    StartDate: Mapped[datetime.date] = mapped_column(DATETIME2)
    EndDate: Mapped[datetime.date] = mapped_column(DATETIME2)
    Premium: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=2))
    Make: Mapped[str] = mapped_column(String(64))
    Model: Mapped[str] = mapped_column(String(64))
    Vin: Mapped[str] = mapped_column(String(17))
    RegistrationNumber: Mapped[str] = mapped_column(String(16))
    BrokerName: Mapped[str] = mapped_column(String(128))
    InsurerName: Mapped[str] = mapped_column(String(128))
