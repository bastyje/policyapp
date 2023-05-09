from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from di_container import DIContainer
from services.insurer_service import InsurerService
from services.models.insurer_creation_model import InsurerCreationModel
from services.models.service_message import ServiceMessage
from webapi.services.authentication import Authentication
from webapi.services.authentication_service import AuthenticationService

router = APIRouter(
    prefix='/insurers',
    tags=['Insurer']
)


@router.post('/')
@inject
def get_all(
        insurer_creation_model: InsurerCreationModel,
        api_key: str,
        insurer_service: InsurerService = Depends(Provide[DIContainer.insurer_service]),
        authentication_service: AuthenticationService = Depends(Provide[DIContainer.authentication_service])
):
    with Authentication(authentication_service, api_key):
        return ServiceMessage(insurer_service.create(insurer_creation_model))

