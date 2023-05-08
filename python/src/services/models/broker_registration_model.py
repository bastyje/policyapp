from pydantic import BaseModel


class BrokerRegistrationModel(BaseModel):
    name: str
