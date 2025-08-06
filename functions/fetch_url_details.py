from .get_db import get_db


def fetch_url_details(alias):
    (con, cur) = get_db()
    res = cur.execute("SELECT alias, url, visits FROM urls WHERE alias = ?", (alias,))
    data = res.fetchone()
    return data
