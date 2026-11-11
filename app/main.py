from fastapi import FastAPI

from app.api.v1.router import router
from app.api.v1.health import health_router


app = FastAPI(title="vLLM")
app.include_router(router)
app.include_router(health_router)