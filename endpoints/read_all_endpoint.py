from fastapi import APIRouter, HTTPException
from functions.get_db import get_db

router = APIRouter()


@router.get("/read_all")
def read_alias():
    (con, cur) = get_db()
    res = cur.execute("SELECT alias, url, visits FROM urls")
    data = res.fetchall()
    if data is None:
        raise HTTPException(status_code=500, detail="Unknown server error")
    aliases = list(map(lambda x: {"alias": x[0], "url": x[1], "visits": x[2]}, data))
    return {"aliases": aliases}
