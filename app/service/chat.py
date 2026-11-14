import json
import httpx
from fastapi import HTTPException
from app.repos.chat import Chat
import os


class ChatService:

    def __init__(self, repo: Chat):

        self.repo = repo
        self.vllm_url = "http://vllm:8000/v1/chat/completions"
        self.model_name = os.getenv("MODEL_NAME")


    async def generate_stream(self, session_id: int, prompt: str):

        session = await self.repo.get_session(session_id)
        if not session:
            raise HTTPException(404)

        await self.repo.create_message(session_id, "user", prompt)

        history = await self.repo.get_history(session_id)

        messages = [{"role": "system", "content": "You are a small talk funny bot"}]

        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": True,
            "max_tokens": 1024,
            "temprature": 0.8
        }

        full_response = ""

        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", self.vllm_url, json=payload) as response:
                if response.status_code != 200:
                    err = await response.aread()
                    raise HTTPException(502, f"{err}")

                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            if delta:
                                full_response += delta
                                yield delta
                        except json.JSONDecodeError:
                            continue

        if full_response:
            await self.repo.create_message(session_id, "assistant", full_response)