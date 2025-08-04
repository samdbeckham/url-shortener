import sqlite3

def get_db():
    con = sqlite3.connect("tmp.db")
    cur = con.cursor()
    return (con, cur)
