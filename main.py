import sqlite3
from typing import Union
from fastapi import FastAPI

tld = "https://url.beckham.io"
app = FastAPI()

def get_db():
    con = sqlite3.connect("tmp.db")
    cur = con.cursor()
    return (con, cur)


def initialize_db():
    (con, cur) = get_db()
    cur.execute("CREATE TABLE urls(alias, url)")
    cur.execute("INSERT INTO urls VALUES ('test', 'https://google.com')")
    con.commit()

@app.get("/test")
def test():
    initialize_db()
    (con, cur) = get_db();
    res = cur.execute("SELECT name FROM sqlite_master")
    return {"test": "success", "alias": res.fetchone()}

@app.get("/{alias_id}")
def read_alias(alias_id: str):
    (con, cur) = get_db()
    res = cur.execute("SELECT alias, url FROM urls")
    (alias, url) = res.fetchone()
    
    # TODO: 302 to the actual URL

    return {"alias": alias, "url": url }

@app.put("/api/shorten")
def shorten_url(alias: str, url: str):
    # TODO: Validation + auth
    # TODO: Store the URL in the database
    return {"short_url": f"{tld}/{alias}", "alias": alias, "url": url }

@app.delete("/api/delete")
def delete_url(alias: str):
    # TODO: Validation + auth
    # TODO: Delete the URL from the database
    return {"alias": alias}

def main():
    print("Hello from url-shortener!")

if __name__ == "__main__":
    main()
