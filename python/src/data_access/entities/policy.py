from typing import List

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.dialects.mssql import DATETIME2, BIT
from sqlalchemy.orm import relationship, mapped_column, Mapped

from data_access.entities import Base


class Policy(Base):
    __tablename__ = 'Policy'
    __table_args__ = {'schema': 'dbo'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    VehicleId: Mapped[int] = mapped_column(ForeignKey('dbo.Vehicle.Id'))
    InsurerId: Mapped[int] = mapped_column(ForeignKey('dbo.Insurer.Id'))
    BrokerId: Mapped[int] = mapped_column(ForeignKey('dbo.Broker.Id'))
    PersonId: Mapped[int] = mapped_column(ForeignKey('dbo.Person.Id'))
    OfferId: Mapped[int] = mapped_column(ForeignKey('dbo.Policy.Id'))
    CreationDate: Mapped[str] = mapped_column(DATETIME2())
    IsOffer: Mapped[bool] = mapped_column(BIT())
    Version: Mapped[int] = mapped_column(Integer())

    PolicyRisks: Mapped[List['PolicyRisk']] = relationship(back_populates='Policy')
    Vehicle: Mapped['Vehicle'] = relationship(back_populates='Policy')
    Insurer: Mapped['Insurer'] = relationship(back_populates='Policies')
    Broker: Mapped['Broker'] = relationship(back_populates='Policies')
    Person: Mapped['Person'] = relationship(back_populates='Policies')
    Offer: Mapped['Policy'] = relationship()
