from functions.get_db import get_db

def setup():
    (con, cur) = get_db()
    cur.execute("CREATE TABLE urls(alias, url)")
    con.commit()

