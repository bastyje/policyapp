from fastapi import FastAPI

from di_container import DIContainer
from webapi.webapi_router import router

def create_app() -> FastAPI:
    app = FastAPI()

    container = DIContainer()
    app.container = container
    app.include_router(router)

    return app
