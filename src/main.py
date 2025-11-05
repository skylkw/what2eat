from fastapi import FastAPI, Response
from core.config import settings
from core.exception import register_exception_handlers
from lifespan import lifespan
from dishes.router import router as dishes_router

app = FastAPI(app_name=settings.app_name, version=settings.version, lifespan=lifespan)
register_exception_handlers(app)

app.include_router(
    router=dishes_router,
)


@app.get("/health")
def health_check():
    return Response(content="OK", media_type="text/plain")
