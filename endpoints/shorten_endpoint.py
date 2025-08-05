from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from functions.fetch_url_details import fetch_url_details
from functions.get_db import get_db

TLD = "https://url.beckham.io"
router = APIRouter()

@router.put("/shorten")
def shorten_url(alias: str, url: str):
    # TODO: Validation, sanitization, + auth

    if fetch_url_details(alias) is not None:
        raise HTTPException(status_code=409, detail="Alias already exists")

    (con, cur) = get_db()
    cur.execute(f"INSERT INTO urls VALUES ('{alias}', '{url}')")
    con.commit()
    return {"short_url": f"{TLD}/{alias}", "alias": alias, "url": url }
