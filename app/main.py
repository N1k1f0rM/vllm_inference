from fastapi import FastAPI

from app.router import router


app = FastAPI(title="vLLM")
app.include_router(router)