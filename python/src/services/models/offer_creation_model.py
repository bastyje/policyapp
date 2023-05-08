import datetime

from pydantic import BaseModel


class VehicleCreationModel(BaseModel):
    make: str
    model: str
    registrationNumber: str
    vin: str
    productionYear: int
    registrationDate: datetime.date
    ownerCount: int


class PersonCreationModel(BaseModel):
    name: str
    lastName: str
    birthDate: datetime.date
    pesel: str
    email: str
    phoneNumber: str


class OfferCreationModel(BaseModel):
    vehicle: VehicleCreationModel
    person: PersonCreationModel
