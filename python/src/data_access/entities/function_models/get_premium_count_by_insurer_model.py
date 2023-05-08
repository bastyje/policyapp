import datetime
from _decimal import Decimal

from sqlalchemy import String, Integer
from sqlalchemy.dialects.mssql import DATETIME2, DECIMAL
from sqlalchemy.orm import mapped_column, Mapped

from data_access.entities import Base


class GetPremiumCountByInsurerModel(Base):
    __table_args__ = {'schema': 'dbo'}
    __tablename__ = 'fntGetPremiumCountByInsurer'

    # Database structure
    PolicyId: Mapped[int] = mapped_column(Integer(), primary_key=True)
    Risk: Mapped[str] = mapped_column(String(128))
    Currency: Mapped[str] = mapped_column(String(128))
    PremiumSum: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=2))
    Make: Mapped[str] = mapped_column(String(64))
    Model: Mapped[str] = mapped_column(String(64))
    Vin: Mapped[str] = mapped_column(String(17))
    RegistrationNumber: Mapped[str] = mapped_column(String(16))
    Name: Mapped[str] = mapped_column(String(128))
    LastName: Mapped[str] = mapped_column(String(128))
    Pesel: Mapped[str] = mapped_column(String(11))
    BrokerName: Mapped[str] = mapped_column(String(128))
