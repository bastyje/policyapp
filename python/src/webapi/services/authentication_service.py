from data_access.repositories.user_repository import UserRepository


class AuthenticationService:
    __user_repository = None

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def authenticate(self, api_key):
        return True if self.__user_repository.get_by_api_key(api_key) is not None else False
