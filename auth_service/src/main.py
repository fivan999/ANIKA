from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from src.dependencies.config import get_db_config
from src.db.base import init_database
from src.routes.users import auth_router


@asynccontextmanager
async def lifespan_events(app: FastAPI):
    """
    Lifespan events of a fastapi application

    Args:
        app (FastAPI): Fastapi application
    """
    app.state.async_sessionmaker = await init_database(
        get_db_config().connection_url
    )
    yield


def get_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """
    Generate openapi scheme for FastAPI app

    Args:
        app (FastAPI): FastAPI application

    Returns:
        Dict[str, Any]: description of openapi schema
    """
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema


def create_app() -> FastAPI:
    """
    Creating Fastapi application object

    Returns:
        FastAPI: Fastapi application
    """
    app = FastAPI(lifespan=lifespan_events)
    app.include_router(auth_router)
    app.openapi_schema = get_openapi_schema(app)
    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handling RequestValidationError

    Args:
        request (Request): fastapi Request object
        exc (RequestValidationError): exception

    Returns:
        JSONResponse
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()[0]['msg']}),
    )
