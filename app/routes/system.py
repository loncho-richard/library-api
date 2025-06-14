from fastapi import APIRouter


router = APIRouter(tags=["System"])


@router.get("health")
async def health_check():
    return {"status": "ok"}


@router.get("/version")
async def get_version():
    return {"version": "1.0.0"}