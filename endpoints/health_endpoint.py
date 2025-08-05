from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from typing import Annotated
from functions.check_key import check_key

router = APIRouter()
header_scheme = APIKeyHeader(name="x-key")

@router.get("/health")
def test_endpoint(key: str = Depends(header_scheme)):
    if (check_key(key)):
        return { "status": "healthy", "key": key }

