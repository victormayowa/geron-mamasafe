from fastapi import APIRouter
from .mothers import router as mothers_router
from .children import router as children_router
from .consultations import router as consultations_router
from .webhooks import router as webhooks_router
from .health_centers import router as health_centers_router
from .providers import router as providers_router
from .messages import router as messages_router

router = APIRouter()

# Include all routers
router.include_router(mothers_router, prefix="/mothers", tags=["Mothers"])
router.include_router(children_router, prefix="/children", tags=["Children"])
router.include_router(consultations_router, prefix="/consultations", tags=["Consultations"])
router.include_router(webhooks_router, prefix="/webhooks", tags=["Webhooks"])
router.include_router(health_centers_router, prefix="/health-centers", tags=["Health Centers"])
router.include_router(providers_router, prefix="/providers", tags=["Health Providers"])
router.include_router(messages_router, prefix="/messages", tags=["Messages"])
