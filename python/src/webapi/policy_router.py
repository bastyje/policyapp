from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from di_container import DIContainer
from services.broker_service import BrokerService
from services.models.offer_creation_model import OfferCreationModel
from services.policy_service import PolicyService
from services.models.offer_template_creation_model import OfferTemplateCreationModel
from services.models.service_message import ServiceMessage
from webapi.services.authentication import Authentication
from webapi.services.authentication_service import AuthenticationService


router = APIRouter(
    prefix='/policies',
    tags=['Policy']
)


@router.get('/')
@inject
def get_by_broker(
        api_key: str,
        is_offer: Optional[bool] = None,
        insurer_id: Optional[int] = None,
        is_summary: Optional[bool] = None,
        person_id: Optional[int] = None,
        vehicle_id: Optional[int] = None,
        policy_service: PolicyService = Depends(Provide[DIContainer.policy_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service])
):
    with Authentication(authentication_service, api_key):
        if insurer_id is not None:
            response = ServiceMessage(policy_service.get_by_insurer(insurer_id, is_summary))
        elif person_id is not None:
            response = ServiceMessage(policy_service.get_by_person(person_id))
        elif vehicle_id is not None:
            response = ServiceMessage(policy_service.get_by_vehicle(vehicle_id))
        else:
            response = ServiceMessage(policy_service.get_by_broker(api_key, is_offer))
        return response


@router.get('/{policy_id}')
@inject
def get_by_id(
        policy_id: int,
        api_key: str,
        policy_service: PolicyService = Depends(Provide[DIContainer.policy_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service])
):
    with Authentication(authentication_service, api_key):
        return ServiceMessage(policy_service.get_by_id(policy_id))


@router.post('/offer-template')
@inject
def create_offer_template(
        offer_template: OfferTemplateCreationModel,
        api_key: str,
        policy_service: PolicyService = Depends(Provide[DIContainer.policy_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service])
):
    with Authentication(authentication_service, api_key):
        return ServiceMessage(policy_service.create_offer_template(offer_template))


@router.post('/offer')
@inject
def create_offer_from_template(
        offer_model: OfferCreationModel,
        policy_offer_template_id: int,
        api_key: str,
        policy_service: PolicyService = Depends(Provide[DIContainer.policy_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service]),
        broker_service: BrokerService = Depends(Provide[DIContainer.broker_service])
):
    with Authentication(authentication_service, api_key):
        service_message = policy_service.create_offer_from_template(
            policy_offer_template_id,
            offer_model,
            broker_service.get_by_api_key(api_key).Id
        )
        res = ServiceMessage(service_message.content, service_message.errors)
        return res


@router.post('/{offer_id}/issue')
@inject
def issue_policy_from_offer(
        offer_id: int,
        api_key: str,
        policy_service: PolicyService = Depends(Provide[DIContainer.policy_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service]),
):
    with Authentication(authentication_service, api_key):
        return ServiceMessage(policy_service.issue_policy(offer_id))
