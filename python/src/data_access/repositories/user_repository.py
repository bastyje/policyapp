from sqlalchemy.exc import NoResultFound

from data_access.database import Database
from data_access.entities.user import User
from data_access.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, User)

    def get_by_api_key(self, api_key: str) -> User | None:
        try:
            return self.session().query(User).filter(User.ApiKey == api_key).one()
        except NoResultFound:
            return None
