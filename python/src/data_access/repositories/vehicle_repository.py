from data_access.database import Database
from data_access.entities.vehicle import Vehicle
from data_access.repositories.base_repository import BaseRepository


class VehicleRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, Vehicle)

    def get_by_vin(self, vin: str) -> Vehicle | None:
        return self.session().query(Vehicle).filter(Vehicle.Vin == vin).first()
