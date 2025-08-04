from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.functions.seed_db import seed_db
from src.functions.get_db import get_db
from src.functions.fetch_url_details import fetch_url_details

tld = "https://url.beckham.io"
app = FastAPI()

@app.get("/test")
def test():
    seed_db()
    (con, cur) = get_db();
    return {"test": "success"}

@app.get("/{alias_id}", response_class=RedirectResponse, status_code=302)
def redirect_to_url(alias_id: str):
    data = fetch_url_details(alias_id)
    if data is None:
        # TODO: Better error handling
        return {"Error": "Notfound"}
    (alias, url) = data
    return url

@app.get("/api/get")
def read_alias(alias_id: str):
    data = fetch_url_details(alias_id)
    if data is None:
        # TODO: Better error handling
        return {"Error": "Notfound"}
    (alias, url) = data
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
