from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from data_access.entities.broker import Broker
from di_container import DIContainer
from services.registration_service import RegistrationService
from services.models.broker_registration_model import BrokerRegistrationModel
from services.models.service_message import ServiceMessage


router = APIRouter(
    prefix='/brokers',
    tags=['Brokers']
)


@router.post('/')
@inject
def register(
        broker_model: BrokerRegistrationModel,
        registration_service: RegistrationService = Depends(Provide[DIContainer.registration_service])
):
    api_key = registration_service.register(broker_model)
    return ServiceMessage({
        'api_key': api_key
    })
