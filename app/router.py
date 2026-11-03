import httpx
from fastapi import APIRouter, HTTPException

from app.models import ChatRequest

MODEL_NAME = "facebook/opt-125m"
VLLM_URL = "http://vllm:8000"

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": req.prompt,
        "max_tokens": req.max_tokens,
        "temperature": req.temprature,
    }

    try:
        async with httpx.AsyncClient(base_url=VLLM_URL, timeout=60.0) as client:
            r = await client.post("/v1/completions", json=payload)
    except httpx.HTTPError as e:
        raise HTTPException(502, f"vLLM unreachable: {e}")

    if r.status_code != 200:
        raise HTTPException(502, f"vLLM returned {r.status_code}: {r.text}")

    return {"text": r.json()["choices"][0]["text"]}