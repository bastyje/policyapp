from sqlalchemy.exc import NoResultFound

from data_access.database import Database
from data_access.entities.broker import Broker
from data_access.repositories.base_repository import BaseRepository


class BrokerRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, Broker)

    def get_by_user_id(self, user_id: int) -> Broker | None:
        try:
            return self.session().query(Broker).filter(Broker.UserId == user_id).one()
        except NoResultFound:
            return None
