from data_access.database import Database
from data_access.entities.person import Person
from data_access.repositories.base_repository import BaseRepository


class PersonRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, Person)

    def get_by_pesel(self, pesel: str):
        return self.session().query(Person).filter(Person.Pesel == pesel).first()
