from sqlalchemy import text

from data_access.database import Database
from data_access.entities.function_models.get_policies_by_broker_model import GetPoliciesByBrokerModel
from data_access.entities.function_models.get_policies_by_insurer_model import GetPoliciesByInsurerModel
from data_access.entities.function_models.get_policies_by_person_model import GetPoliciesByPersonModel
from data_access.entities.function_models.get_policies_by_vehicle_model import GetPoliciesByVehicleModel
from data_access.entities.function_models.get_premium_count_by_insurer_model import GetPremiumCountByInsurerModel
from data_access.entities.policy import Policy
from data_access.repositories.base_repository import BaseRepository


class PolicyRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, Policy)

    def get_by_broker(self, broker_id: int, is_offer: bool = False):
        result = self.session()\
            .query(GetPoliciesByBrokerModel)\
            .params(broker_id=broker_id, is_offer=is_offer)\
            .from_statement(text('SELECT * FROM dbo.fntGetPoliciesByBroker(:broker_id, :is_offer)'))\
            .all()
        return result

    def get_by_insurer(self, insurer_id: int):
        result = self.session()\
            .query(GetPoliciesByInsurerModel)\
            .params(insurer_id=insurer_id)\
            .from_statement(text('SELECT * FROM dbo.fntGetPoliciesByInsurer(:insurer_id)'))\
            .all()
        return result

    def get_by_person(self, person_id: int):
        result = self.session()\
            .query(GetPoliciesByPersonModel)\
            .params(person_id=person_id)\
            .from_statement(text('SELECT * FROM dbo.fntGetPoliciesByPerson(:person_id)'))\
            .all()
        return result

    def get_by_vehicle(self, vehicle_id: int):
        result = self.session()\
            .query(GetPoliciesByVehicleModel)\
            .params(vehicle_id=vehicle_id)\
            .from_statement(text('SELECT * FROM dbo.fntGetPoliciesByVehicle(:vehicle_id)'))\
            .all()
        return result

    def get_premium_sum_by_insurer(self, insurer_id: int):
        result = self.session()\
            .query(GetPremiumCountByInsurerModel)\
            .params(insurer_id=insurer_id)\
            .from_statement(text('SELECT * FROM dbo.fntGetPremiumCountByInsurer(:insurer_id)'))\
            .all()
        return result
