from .get_db import get_db

def seed_db():
    (con, cur) = get_db()
    cur.execute("CREATE TABLE urls(alias, url)")
    cur.execute("INSERT INTO urls VALUES ('testalias1', 'https://google.com')")
    cur.execute("INSERT INTO urls VALUES ('testalias2', 'https://netflix.com')")
    con.commit()
