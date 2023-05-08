from dependency_injector import containers, providers

from config_reader import ConfigReader
from data_access.database import Database
from data_access.repositories.broker_repository import BrokerRepository
from data_access.repositories.insurer_repository import InsurerRepository
from data_access.repositories.person_repository import PersonRepository
from data_access.repositories.policy_offer_template_repository import PolicyOfferTemplateRepository
from data_access.repositories.policy_repository import PolicyRepository
from data_access.repositories.policy_risk_repository import PolicyRiskRepository
from data_access.repositories.user_repository import UserRepository
from data_access.repositories.vehicle_repository import VehicleRepository
from services.broker_service import BrokerService
from services.calculation_service import CalculationService
from services.insurer_service import InsurerService
from services.policy_service import PolicyService
from services.registration_service import RegistrationService
from webapi.services.authentication_service import AuthenticationService


class DIContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            'webapi.policy_router',
            'webapi.broker_router',
            'webapi.insurer_router'
        ]
    )

    config = providers.Singleton(ConfigReader)

    # REPOSITORIES

    database = providers.Factory(
        Database,
        config=config
    )

    broker_repository = providers.Factory(
        BrokerRepository,
        database=database
    )

    insurer_repository = providers.Factory(
        InsurerRepository,
        database=database
    )

    person_repository = providers.Factory(
        PersonRepository,
        database=database
    )

    policy_offer_template_repository = providers.Factory(
        PolicyOfferTemplateRepository,
        database=database
    )

    policy_repository = providers.Factory(
        PolicyRepository,
        database=database
    )

    policy_risk_repository = providers.Factory(
        PolicyRiskRepository,
        database=database
    )

    user_repository = providers.Factory(
        UserRepository,
        database=database
    )

    vehicle_repository = providers.Factory(
        VehicleRepository,
        database=database
    )

    # SERVICES

    authentication_service = providers.Factory(
        AuthenticationService,
        user_repository=user_repository
    )

    broker_service = providers.Factory(
        BrokerService,
        broker_repository=broker_repository,
        user_repository=user_repository
    )

    insurer_service = providers.Factory(
        InsurerService,
        insurer_repository=insurer_repository
    )

    calculation_service = providers.Factory(
        CalculationService
    )

    policy_service = providers.Factory(
        PolicyService,
        policy_repository=policy_repository,
        broker_service=broker_service,
        policy_offer_template_repository=policy_offer_template_repository,
        vehicle_repository=vehicle_repository,
        policy_risk_repository=policy_risk_repository,
        calculation_service=calculation_service,
        person_repository=person_repository
    )

    registration_service = providers.Factory(
        RegistrationService,
        user_repository=user_repository,
        broker_repository=broker_repository
    )

