import validators
from fastapi import APIRouter, HTTPException
from functions.fetch_url_details import fetch_url_details
from functions.get_db import get_db

TLD = "https://url.beckham.io"
router = APIRouter()


@router.put("/shorten")
def shorten_url(alias: str, url: str):
    if fetch_url_details(alias) is not None:
        raise HTTPException(status_code=409, detail="Alias already exists")

    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    (con, cur) = get_db()
    cur.execute("INSERT INTO urls VALUES (?, ?)", (alias, url))
    con.commit()
    return {"short_url": f"{TLD}/{alias}", "alias": alias, "url": url}
