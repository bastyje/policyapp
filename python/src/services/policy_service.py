import datetime
from typing import List

from sqlalchemy.orm import make_transient

from data_access.entities.person import Person
from data_access.entities.policy import Policy
from data_access.entities.policy_offer_template import PolicyOfferTemplate
from data_access.entities.policy_risk import PolicyRisk
from data_access.entities.vehicle import Vehicle
from data_access.repositories.person_repository import PersonRepository
from data_access.repositories.policy_offer_template_repository import PolicyOfferTemplateRepository
from data_access.repositories.policy_repository import PolicyRepository
from data_access.repositories.policy_risk_repository import PolicyRiskRepository
from data_access.repositories.vehicle_repository import VehicleRepository
from services.broker_service import BrokerService
from services.calculation_service import CalculationService
from services.errors import Errors
from services.models.offer_template_creation_model import OfferTemplateCreationModel
from services.models.service_message import ServiceMessage
from services.models.offer_creation_model import OfferCreationModel


class PolicyService:
    __person_repository: PersonRepository
    __policy_repository: PolicyRepository
    __policy_offer_template_repository: PolicyOfferTemplateRepository
    __policy_risk_repository: PolicyRiskRepository
    __vehicle_repository: VehicleRepository

    __broker_service: BrokerService
    __calculation_service: CalculationService

    def __init__(
            self,
            policy_repository: PolicyRepository,
            broker_service: BrokerService,
            policy_offer_template_repository: PolicyOfferTemplateRepository,
            vehicle_repository: VehicleRepository,
            calculation_service: CalculationService,
            policy_risk_repository: PolicyRiskRepository,
            person_repository: PersonRepository
    ):
        self.__policy_repository = policy_repository
        self.__broker_service = broker_service
        self.__policy_offer_template_repository = policy_offer_template_repository
        self.__vehicle_repository = vehicle_repository
        self.__calculation_service = calculation_service
        self.__policy_risk_repository = policy_risk_repository
        self.__person_repository = person_repository

    def get_by_broker(self, api_key: str, is_offer: bool = False) -> [Policy]:
        broker = self.__broker_service.get_by_api_key(api_key)
        if broker is None:
            return []

        return self.__policy_repository.get_by_broker(broker.Id, is_offer)

    def get_by_id(self, policy_id: int) -> [Policy]:
        return self.__policy_repository.get_by_id(policy_id)

    def get_by_vehicle(self, vehicle_id: int):
        return self.__policy_repository.get_by_vehicle(vehicle_id)

    def get_by_person(self, person_id: int):
        return self.__policy_repository.get_by_person(person_id)

    def get_by_insurer(self, insurer_id: int, is_summary: bool):
        return self.__policy_repository.get_premium_sum_by_insurer(insurer_id)\
            if is_summary\
            else self.__policy_repository.get_by_insurer(insurer_id)

    def create_offer_template(self, offer_template_model: OfferTemplateCreationModel) -> int:
        policy_offer_template = PolicyOfferTemplate()
        policy_offer_template.Id = self.__policy_offer_template_repository.create_id()
        policy_offer_template.Name = offer_template_model.name
        policy_offer_template.InsurerId = offer_template_model.insurerId
        policy_offer_template.QuotationAlgorithm = offer_template_model.quotationAlgorithm
        policy_offer_template.ValidFrom = offer_template_model.validFrom
        policy_offer_template.ValidTo = offer_template_model.validTo

        self.__policy_offer_template_repository.session().add(policy_offer_template)
        self.__policy_offer_template_repository.session().commit()

        return policy_offer_template.Id

    def create_offer_from_template(self, template_id: int, offer_model: OfferCreationModel, broker_id: int) -> ServiceMessage:
        service_message = ServiceMessage()

        template = self.__policy_offer_template_repository.get_by_id(template_id)
        if template is None:
            service_message.errors.append(Errors.NO_POLICY_OFFER_TEMPLATE)
            return service_message

        vehicle = self.__vehicle_repository.get_by_vin(offer_model.vehicle.vin)
        if vehicle is None:
            vehicle = Vehicle()
            vehicle.Id = self.__vehicle_repository.create_id()
            vehicle.Make = offer_model.vehicle.make
            vehicle.Model = offer_model.vehicle.model
            vehicle.RegistrationNumber = offer_model.vehicle.registrationNumber
            vehicle.Vin = offer_model.vehicle.vin
            vehicle.ProductionYear = offer_model.vehicle.productionYear
            vehicle.RegistrationDate = offer_model.vehicle.registrationDate
            vehicle.OwnerCount = offer_model.vehicle.ownerCount
            self.__vehicle_repository.session().add(vehicle)
            self.__vehicle_repository.session().commit()

        person = self.__person_repository.get_by_pesel(offer_model.person.pesel)
        if person is None:
            person = Person()
            person.Id = self.__person_repository.create_id()
            person.Name = offer_model.person.name
            person.LastName = offer_model.person.lastName
            person.BirthDate = offer_model.person.birthDate
            person.Pesel = offer_model.person.pesel
            person.Email = offer_model.person.email
            person.PhoneNumber = offer_model.person.phoneNumber
            self.__person_repository.session().add(person)
            self.__person_repository.session().commit()

        offer = Policy()
        offer.Id = self.__policy_repository.create_id()
        offer.VehicleId = vehicle.Id
        offer.InsurerId = template.InsurerId
        offer.BrokerId = broker_id
        offer.PersonId = person.Id
        offer.CreationDate = datetime.date.today()
        offer.IsOffer = True
        offer.Version = 1
        self.__policy_repository.session().add(offer)
        self.__policy_repository.session().commit()

        risks = self.calculate_risks(vehicle, template)

        for index, risk in enumerate(risks):
            risks[index].PolicyId = offer.Id
            risks[index].Id = self.__policy_risk_repository.create_id()
            self.__policy_risk_repository.session().add(risks[index])

        self.__policy_risk_repository.session().commit()

        service_message.content = offer.Id
        return service_message

    def issue_policy(self, offer_id: int) -> ServiceMessage:
        service_message = ServiceMessage()

        offer = self.__policy_repository.get_by_id(offer_id)
        if not offer.IsOffer:
            service_message.errors.append(Errors.NO_OFFER_WITH_ID)
        else:
            risks = offer.PolicyRisks
            make_transient(offer)
            policy = offer
            policy.OfferId = offer.Id
            policy.Id = self.__policy_repository.create_id()
            policy.IsOffer = False
            self.__policy_repository.session().add(policy)
            self.__policy_repository.session().commit()

            for index, risk in enumerate(risks):
                new_risk = PolicyRisk()
                new_risk.Id = self.__policy_risk_repository.create_id()
                new_risk.PolicyId = policy.Id
                new_risk.CurrencyId = risk.CurrencyId
                new_risk.RiskId = risk.RiskId
                new_risk.CreationDate = datetime.date.today()
                new_risk.StartDate = risk.StartDate
                new_risk.EndDate = risk.EndDate
                new_risk.Premium = risk.Premium
                self.__policy_risk_repository.session().add(new_risk)

            self.__policy_risk_repository.session().commit()
            service_message.content = offer.Id

        return service_message

    def calculate_risks(self, vehicle: Vehicle, policy_offer_template: PolicyOfferTemplate) -> list[PolicyRisk]:
        return self.__calculation_service.calculate(vehicle, policy_offer_template)
