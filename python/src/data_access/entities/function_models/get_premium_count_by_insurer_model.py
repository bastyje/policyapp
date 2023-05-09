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
    Risk: Mapped[str] = mapped_column(String(128))
    Currency: Mapped[str] = mapped_column(String(128), primary_key=True)
    PremiumSum: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=2), primary_key=True)
    BrokerName: Mapped[str] = mapped_column(String(128), primary_key=True)
