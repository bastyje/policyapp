from data_access.database import Database
from data_access.entities.insurer import Insurer
from data_access.repositories.base_repository import BaseRepository


class InsurerRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, Insurer)
