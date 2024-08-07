from fastapi import FastAPI

from src.routers import permissions, subscriptions, topics


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(topics.topic_router)
    app.include_router(permissions.permission_router)
    app.include_router(subscriptions.subscription_router)
    return app


app = create_app()
