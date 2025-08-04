from fastapi import APIRouter
from functions.get_db import get_db

router = APIRouter()

@router.delete("/delete")
def delete_url(alias_id: str):
    # TODO: Validation + auth
    (con,cur) = get_db()
    cur.execute(f"DELETE FROM urls WHERE alias = '{alias_id}'")
    con.commit()
    return {"alias": alias_id}

