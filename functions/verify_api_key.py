import os
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

header_scheme = APIKeyHeader(name="x-key")


def verify_api_key(api_key: str = Depends(header_scheme)):
    if not api_key == os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key
