import enum

from data_access.entities.dict.base_dict import BaseDict


class CurrencyEnum(enum.Enum):
    EUR = 1
    PLN = 2
    USD = 3


class Currency(BaseDict):
    __tablename__ = 'Currency'
    __table_args__ = {'schema': 'dict'}
