from .get_db import get_db

def fetch_url_details(alias_id):
    (con, cur) = get_db()
    res = cur.execute(f"SELECT alias, url FROM urls WHERE alias = '{alias_id}'")
    data = res.fetchone()
    return data
