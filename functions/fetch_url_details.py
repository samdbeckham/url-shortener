from .get_db import get_db

def fetch_url_details(alias):
    (con, cur) = get_db()
    res = cur.execute(f"SELECT alias, url FROM urls WHERE alias = '{alias}'")
    data = res.fetchone()
    return data
