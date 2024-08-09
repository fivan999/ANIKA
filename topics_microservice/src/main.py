from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import partners, permissions, subscriptions, topics


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(topics.topic_router)
    app.include_router(permissions.permission_router)
    app.include_router(subscriptions.subscription_router)
    app.include_router(partners.partner_router)
    return app


app = create_app()
