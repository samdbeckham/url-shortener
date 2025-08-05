from functions.get_db import get_db

def teardown():
    (con, cur) = get_db()
    cur.execute("DROP TABLE IF EXISTS urls")

