import sqlite3
from typing import Union
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

tld = "https://url.beckham.io"
app = FastAPI()

def get_db():
    con = sqlite3.connect("tmp.db")
    cur = con.cursor()
    return (con, cur)


def initialize_db():
    (con, cur) = get_db()
    cur.execute("CREATE TABLE urls(alias, url)")
    cur.execute("INSERT INTO urls VALUES ('testalias1', 'https://google.com')")
    cur.execute("INSERT INTO urls VALUES ('testalias2', 'https://netflix.com')")
    con.commit()

def fetch_url_details(alias_id):
    (con, cur) = get_db()
    res = cur.execute(f"SELECT alias, url FROM urls WHERE alias = '{alias_id}'")
    data = res.fetchone()
    if data is None:
        # TODO: Better error handling
        return {"Error": "Notfound"}
    return data;

@app.get("/test")
def test():
    initialize_db()
    (con, cur) = get_db();
    res = cur.execute("SELECT name FROM sqlite_master")
    return {"test": "success", "alias": res.fetchone()}

@app.get("/{alias_id}", response_class=RedirectResponse, status_code=302)
def redirect_to_url(alias_id: str):
    (alias, url) = fetch_url_details(alias_id)
    return url

@app.get("/api/get")
def read_alias(alias_id: str):
    (alias, url) = fetch_url_details(alias_id)
    return {"alias": alias, "url": url }

@app.put("/api/shorten")
def shorten_url(alias: str, url: str):
    # TODO: Validation, sanitization, + auth
    (con, cur) = get_db()
    cur.execute(f"INSERT INTO urls VALUES ('{alias}', '{url}')")
    con.commit()

    return {"short_url": f"{tld}/{alias}", "alias": alias, "url": url }

@app.delete("/api/delete")
def delete_url(alias_id: str):
    # TODO: Validation + auth
    (con,cur) = get_db()
    cur.execute(f"DELETE FROM urls WHERE alias = '{alias_id}'")
    con.commit()

    return {"alias": alias_id}

def main():
    print("Hello from url-shortener!")

if __name__ == "__main__":
    main()
