from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_endpoint():
    return { "status": "healthy" }
