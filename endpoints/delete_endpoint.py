from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from functions.fetch_url_details import fetch_url_details
from functions.get_db import get_db

router = APIRouter()

@router.delete("/delete")
def delete_url(alias: str):
    # TODO: Validation + auth
    if fetch_url_details(alias) is None:
        raise HTTPException(status_code=404, detail="Alias not found")

    (con,cur) = get_db()
    cur.execute(f"DELETE FROM urls WHERE alias = '{alias}'")
    con.commit()
    return {"detail": "Alias deleted"}

