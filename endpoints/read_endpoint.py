from fastapi import APIRouter, HTTPException
from functions.fetch_url_details import fetch_url_details

router = APIRouter()

@router.get("/read")
def read_alias(alias: str):
    data = fetch_url_details(alias)
    if data is None:
        raise HTTPException(status_code=404, detail="Alias not found")
    (_, url) = data
    return {"alias": alias, "url": url }
