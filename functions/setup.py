from functions.get_db import get_db


def setup():
    (con, cur) = get_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls(
            alias VARCHAR(32),
            url VARCHAR(256),
            visits INT
        )
    """)
    con.commit()
