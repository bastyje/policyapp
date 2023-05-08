from fastapi import APIRouter

from webapi.policy_router import router as policy_router
from webapi.broker_router import router as broker_router
from webapi.insurer_router import router as insurer_router


router = APIRouter()
router.include_router(policy_router)
router.include_router(broker_router)
router.include_router(insurer_router)
