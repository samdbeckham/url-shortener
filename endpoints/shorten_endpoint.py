import validators
from fastapi import APIRouter, HTTPException
from functions.fetch_url_details import fetch_url_details
from functions.get_db import get_db
from functions.generate_alias import generate_alias

TLD = "https://url.beckham.io"
router = APIRouter()


@router.put("/shorten")
def shorten_url(url: str, alias: str = None):
    if fetch_url_details(alias) is not None and alias is not None:
        raise HTTPException(status_code=409, detail="Alias already exists")

    # NOTE: We loop here to make sure the random alias isn't already taken
    #       In most instances, this loop will only run once.
    if alias is None:
        while True:
            alias = generate_alias()
            if fetch_url_details(alias) is None:
                break

    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    (con, cur) = get_db()
    cur.execute("INSERT INTO urls VALUES (?, ?, 0)", (alias, url))
    con.commit()
    return {"short_url": f"{TLD}/{alias}", "alias": alias, "url": url}
