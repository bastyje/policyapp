import enum

from data_access.entities.dict.base_dict import BaseDict


class RiskEnum(enum.Enum):
    TPL = 1
    Casco = 2
    Assistance = 3
    GAP = 4


class Risk(BaseDict):
    __tablename__ = 'Risk'
    __table_args__ = {'schema': 'dict'}
