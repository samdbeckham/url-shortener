from fastapi import FastAPI
from functions.seed_db import seed_db
from functions.get_db import get_db
from functions.fetch_url_details import fetch_url_details
from endpoints import (
    delete_endpoint,
    health_endpoint,
    read_all_endpoint,
    read_endpoint,
    redirect_endpoint,
    shorten_endpoint,
)
from functions.setup import setup

api_prefix = "/api"
app = FastAPI()

setup()

app.include_router(redirect_endpoint.router)
app.include_router(health_endpoint.router, prefix=api_prefix)
app.include_router(read_all_endpoint.router, prefix=api_prefix)
app.include_router(read_endpoint.router, prefix=api_prefix)
app.include_router(shorten_endpoint.router, prefix=api_prefix)
app.include_router(delete_endpoint.router, prefix=api_prefix)
