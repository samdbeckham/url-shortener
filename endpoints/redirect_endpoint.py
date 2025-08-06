from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from functions.fetch_url_details import fetch_url_details

router = APIRouter()


@router.get("/{alias}", response_class=RedirectResponse, status_code=302)
def redirect_to_url(alias: str):
    data = fetch_url_details(alias)
    if data is None:
        raise HTTPException(status_code=404, detail="Alias not found")
    url = data[1]
    return url
