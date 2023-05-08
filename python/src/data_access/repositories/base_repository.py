from typing import Any

from sqlalchemy.exc import NoResultFound

from data_access.database import Database


class BaseRepository:
    __database: Database
    __entity_type = None

    def __init__(self, database: Database, entity_type: Any):
        self.__database = database
        self.__entity_type = entity_type

    def session(self):
        return self.__database.session()

    def create_id(self):
        entity = self.session().query(self.__entity_type).order_by(self.__entity_type.Id.desc()).first()
        return 1 if entity is None else entity.Id + 1

    def get_by_id(self, entity_id: int):
        return self.session().query(self.__entity_type).filter(self.__entity_type.Id == entity_id).first()
