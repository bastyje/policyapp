from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from data_access.entities import Base


class Insurer(Base):
    __tablename__ = 'Insurer'
    __table_args__ = {'schema': 'dbo'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    Name: Mapped[str] = mapped_column(String(128))
    Krs: Mapped[str] = mapped_column(String(10))
    TaxId: Mapped[str] = mapped_column(String(10))

    PolicyOfferTemplates: Mapped[List['PolicyOfferTemplate']] = relationship(back_populates='Insurer')
    Policies: Mapped[List['Policy']] = relationship(back_populates='Insurer')
