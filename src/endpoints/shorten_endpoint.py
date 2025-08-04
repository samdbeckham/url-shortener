from fastapi import APIRouter
from ..functions.get_db import get_db

router = APIRouter()

@router.put("/shorten")
def shorten_url(alias: str, url: str):
    # TODO: Validation, sanitization, + auth
    (con, cur) = get_db()
    cur.execute(f"INSERT INTO urls VALUES ('{alias}', '{url}')")
    con.commit()
    return {"short_url": f"{tld}/{alias}", "alias": alias, "url": url }
