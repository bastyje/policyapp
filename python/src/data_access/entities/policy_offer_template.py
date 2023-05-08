import datetime

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.entities import Base


class PolicyOfferTemplate(Base):
    __tablename__ = 'PolicyOfferTemplate'
    __table_args__ = {'schema': 'conf'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    Name: Mapped[str] = mapped_column(String(128))
    InsurerId: Mapped[int] = mapped_column(ForeignKey('dbo.Insurer.Id'))
    QuotationAlgorithm: Mapped[str] = mapped_column(String())
    ValidFrom: Mapped[datetime.date] = mapped_column(DATETIME2())
    ValidTo: Mapped[datetime.date] = mapped_column(DATETIME2())

    Insurer: Mapped['Insurer'] = relationship(back_populates='PolicyOfferTemplates')
