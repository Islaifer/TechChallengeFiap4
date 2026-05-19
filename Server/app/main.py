from app.core.config import settings
from app.core.config.redis_connection import get_redis_connection
from app.api.router import predict_controller
from app.core.startup.bootstrap import init
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

async def lifespan(app: FastAPI):
    await init()
    app.include_router(predict_controller.router)

    yield

    redis = get_redis_connection()
    await redis.close()

    
app = FastAPI(
    title = settings.SERVICE_NAME,
    version = settings.VERSION,
    description = settings.DESCRIPTION,
    lifespan=lifespan
)

Instrumentator().instrument(app).expose(app)