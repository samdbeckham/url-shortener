from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def test_endpoint():
    return { "status": "healthy" }
