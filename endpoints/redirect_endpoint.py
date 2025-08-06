from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from functions.fetch_url_details import fetch_url_details
from functions.get_db import get_db

router = APIRouter()


@router.get("/{alias}", response_class=RedirectResponse, status_code=302)
def redirect_to_url(alias: str):
    data = fetch_url_details(alias)
    if data is None:
        raise HTTPException(status_code=404, detail="Alias not found")

    (_, url, visits) = data
    (con, cur) = get_db()
    cur.execute("UPDATE urls SET visits = ? WHERE alias = ?", (visits + 1, alias))
    con.commit()

    return url
