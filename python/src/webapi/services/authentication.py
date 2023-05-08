from fastapi import HTTPException

from webapi.services.authentication_service import AuthenticationService


class Authentication:
    __authentication_service = None
    __api_key = None

    def __init__(self, authentication_service: AuthenticationService, api_key: str):
        self.__authentication_service = authentication_service
        self.__api_key = api_key

    def __enter__(self):
        if not self.__authentication_service.authenticate(self.__api_key):
            raise HTTPException(status_code=401)

        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
