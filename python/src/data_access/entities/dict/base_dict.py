from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class BaseDict:
    Id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    Name: Mapped[str] = mapped_column(String(128))
