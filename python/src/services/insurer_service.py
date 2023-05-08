from data_access.entities.insurer import Insurer
from data_access.repositories.insurer_repository import InsurerRepository
from services.models.insurer_creation_model import InsurerCreationModel


class InsurerService:
    __insurer_repository: InsurerRepository

    def __init__(self, insurer_repository: InsurerRepository):
        self.__insurer_repository = insurer_repository

    def create(self, insurer_creation_model: InsurerCreationModel):
        insurer = Insurer()
        insurer.Id = self.__insurer_repository.create_id()
        insurer.Name = insurer_creation_model.name
        insurer.Krs = insurer_creation_model.krs
        insurer.TaxId = insurer_creation_model.taxId

        self.__insurer_repository.session().add(insurer)
        self.__insurer_repository.session().commit()

        return insurer.Id
