from data_access.database import Database
from data_access.entities.policy_risk import PolicyRisk
from data_access.repositories.base_repository import BaseRepository


class PolicyRiskRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, PolicyRisk)
