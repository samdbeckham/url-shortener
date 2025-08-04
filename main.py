from fastapi import FastAPI
from functions.seed_db import seed_db
from functions.get_db import get_db
from functions.fetch_url_details import fetch_url_details
from endpoints import (
    delete_endpoint,
    health_endpoint,
    read_endpoint,
    redirect_endpoint,
    shorten_endpoint,
    test_endpoint,
)

api_prefix = "/api"
app = FastAPI()

app.include_router(redirect_endpoint.router)
app.include_router(test_endpoint.router, prefix=api_prefix)
app.include_router(health_endpoint.router, prefix=api_prefix)
app.include_router(read_endpoint.router, prefix=api_prefix)
app.include_router(shorten_endpoint.router, prefix=api_prefix)
app.include_router(delete_endpoint.router, prefix=api_prefix)

def main():
    print("Hello from url-shortener!")

if __name__ == "__main__":
    main()
