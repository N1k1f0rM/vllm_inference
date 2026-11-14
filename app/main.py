from fastapi import FastAPI

from app.api.v1.chat import chat_router
from app.api.v1.health import health_router


app = FastAPI(title="vLLM")
app.include_router(chat_router)
app.include_router(health_router)