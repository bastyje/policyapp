from data_access.entities.broker import Broker
from data_access.repositories.broker_repository import BrokerRepository
from data_access.repositories.user_repository import UserRepository


class BrokerService:
    __broker_repository: BrokerRepository
    __user_repository: UserRepository

    def __init__(self, broker_repository: BrokerRepository, user_repository: UserRepository):
        self.__broker_repository = broker_repository
        self.__user_repository = user_repository

    def get_by_api_key(self, api_key: str) -> Broker | None:
        user = self.__user_repository.get_by_api_key(api_key)

        if user is None:
            return None

        return self.__broker_repository.get_by_user_id(user.Id)
