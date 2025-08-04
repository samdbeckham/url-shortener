from fastapi import APIRouter
from functions.seed_db import seed_db

router = APIRouter()

@router.get("/test")
def test_endpoint():
    seed_db()
    return {"test": "success"}
