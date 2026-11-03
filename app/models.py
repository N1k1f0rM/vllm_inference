from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChatRequest(BaseModel):
    prompt: str = Field(..., examples=["Moscow is a capital"])
    max_tokens: int = Field(64, ge=1, le=128)
    temprature: float = Field(0.7)