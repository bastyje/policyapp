from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from data_access.entities import Base


class Broker(Base):
    __tablename__ = 'Broker'
    __table_args__ = {'schema': 'dbo'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    Name: Mapped[str] = mapped_column(String(128))
    UserId: Mapped[int] = mapped_column(Integer(), ForeignKey('security.User.Id'))

    # User: Mapped['User'] = relationship(back_populates='Broker')
    Policies: Mapped['Policy'] = relationship(back_populates='Broker')
