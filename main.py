from fastapi import FastAPI
from src.functions.seed_db import seed_db
from src.functions.get_db import get_db
from src.functions.fetch_url_details import fetch_url_details
from src.endpoints import (
    delete_endpoint,
    read_endpoint,
    redirect_endpoint,
    shorten_endpoint,
    test_endpoint,
)

tld = "https://url.beckham.io"
api_prefix = "/api"
app = FastAPI()

app.include_router(redirect_endpoint.router)
app.include_router(test_endpoint.router, prefix=api_prefix)
app.include_router(read_endpoint.router, prefix=api_prefix)
app.include_router(shorten_endpoint.router, prefix=api_prefix)
app.include_router(delete_endpoint.router, prefix=api_prefix)

def main():
    print("Hello from url-shortener!")

if __name__ == "__main__":
    main()
