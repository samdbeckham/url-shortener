from fastapi import FastAPI, Depends
from functions.setup import setup
from functions.verify_api_key import verify_api_key
from endpoints import (
    delete_endpoint,
    health_endpoint,
    read_all_endpoint,
    read_endpoint,
    redirect_endpoint,
    shorten_endpoint,
)

api_prefix = "/api"
app = FastAPI()

setup()

app.include_router(redirect_endpoint.router)
app.include_router(health_endpoint.router, prefix=api_prefix, dependencies=[Depends(verify_api_key)])
app.include_router(read_all_endpoint.router, prefix=api_prefix)
app.include_router(read_endpoint.router, prefix=api_prefix)
app.include_router(shorten_endpoint.router, prefix=api_prefix)
app.include_router(delete_endpoint.router, prefix=api_prefix)
