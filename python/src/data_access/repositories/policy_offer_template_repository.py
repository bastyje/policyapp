from data_access.database import Database
from data_access.entities.policy_offer_template import PolicyOfferTemplate
from data_access.repositories.base_repository import BaseRepository


class PolicyOfferTemplateRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, PolicyOfferTemplate)
