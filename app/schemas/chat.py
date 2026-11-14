from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SessionCreate(BaseModel):

    title: str = "New chat"


class SessionRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    created_at: datetime


class MessageRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class ChatRequest(BaseModel):

    prompt: str
