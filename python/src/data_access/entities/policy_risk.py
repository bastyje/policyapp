import datetime
from _decimal import Decimal

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.dialects.mssql import DATETIME2, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.entities import Base


class PolicyRisk(Base):
    __tablename__ = 'PolicyRisk'
    __table_args__ = {'schema': 'dbo'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    PolicyId: Mapped[int] = mapped_column(Integer(), ForeignKey('dbo.Policy.Id'))
    CurrencyId: Mapped[int] = mapped_column(Integer()) # , ForeignKey('dict.Currency.Id'))
    RiskId: Mapped[int] = mapped_column(Integer()) # , ForeignKey('dict.Risk.Id'))
    CreationDate: Mapped[datetime.date] = mapped_column(DATETIME2())
    StartDate: Mapped[datetime.date] = mapped_column(DATETIME2())
    EndDate: Mapped[datetime.date] = mapped_column(DATETIME2())
    Premium: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=2))

    Policy: Mapped['Policy'] = relationship(back_populates='PolicyRisks')
    # Currency: Mapped['Currency'] = relationship()
    # Risk: Mapped['Risk'] = relationship()
