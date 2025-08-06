import os
import sqlite3


def get_db():
    con = sqlite3.connect(os.getenv("DATABASE_NAME", "tmp.db"))
    cur = con.cursor()
    return (con, cur)
