from fastapi import APIRouter

from app.health.responses import PingResponse

router = APIRouter(tags=["health"], prefix="/health")


@router.get("/ping")
def ping() -> PingResponse:
    return PingResponse(message="pong")
