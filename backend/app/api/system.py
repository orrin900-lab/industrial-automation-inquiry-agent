from fastapi import APIRouter

from app.services.system_service import get_system_status


router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status")
def get_system_status_endpoint() -> dict:
    return get_system_status().model_dump(mode="json")
