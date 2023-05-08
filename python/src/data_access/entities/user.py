from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.entities import Base


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'security'}

    # Database structure
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=False)
    ApiKey: Mapped[str] = mapped_column(String(512))

    # Broker: Mapped['Broker'] = relationship(back_populates='User')
