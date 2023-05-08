import string
import random

from data_access.entities.broker import Broker
from data_access.entities.user import User
from data_access.repositories.broker_repository import BrokerRepository
from data_access.repositories.user_repository import UserRepository
from services.models.broker_registration_model import BrokerRegistrationModel


class RegistrationService:
    __user_repository = None
    __broker_repository = None

    def __init__(self, user_repository: UserRepository, broker_repository: BrokerRepository):
        self.__broker_repository = broker_repository
        self.__user_repository = user_repository

    def register(self, broker_model: BrokerRegistrationModel) -> str:
        user = User()
        user.Id = self.__user_repository.create_id()
        user.ApiKey = self.create_api_key()
        self.__user_repository.session().add(user)
        self.__user_repository.session().commit()

        broker = Broker()
        broker.Id = self.__broker_repository.create_id()
        broker.Name = broker_model.name
        broker.UserId = user.Id
        self.__broker_repository.session().add(broker)
        self.__broker_repository.session().commit()

        return user.ApiKey

    def create_api_key(self) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(512))


