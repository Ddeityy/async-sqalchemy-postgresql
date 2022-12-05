from database import db
from fastapi import FastAPI


def init_app():
    db.init()

    app = FastAPI(
        title="Users App",
        description="Handling Our User",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from views import users_api, orders_api

    app.include_router(
        users_api,
        prefix="/api/v1",
    )

    app.include_router(
        orders_api,
        prefix="/api/v1",
    )

    return app


app = init_app()
