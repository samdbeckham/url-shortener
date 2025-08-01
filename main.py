from typing import Union
from fastapi import FastAPI

tld = "https://url.beckham.io"
app = FastAPI()

@app.get("/{alias}")
def read_alias(alias: str):
    # TODO: Fetch the URL from the database
    # TODO: 302 to the actual URL
    return {"alias": alias, "url": "https://google.com" }

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
