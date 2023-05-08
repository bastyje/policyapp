import datetime
from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import mapped_column, Mapped, relationship

from data_access.entities import Base


class Person(Base):
    __tablename__ = 'Person'
    __table_args__ = {'schema': 'dbo'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    Name: Mapped[str] = mapped_column(String(128))
    LastName: Mapped[str] = mapped_column(String(128))
    BirthDate: Mapped[datetime.datetime] = mapped_column(DATETIME2())
    Pesel: Mapped[str] = mapped_column(String(11))
    Email: Mapped[str] = mapped_column(String(128))
    PhoneNumber: Mapped[str] = mapped_column(String(9))

    Policies: Mapped[List['Policy']] = relationship(back_populates='Person')
