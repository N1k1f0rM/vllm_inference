from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.repos.chat import Chat
from app.service.chat import ChatService
from app.schemas.chat import SessionCreate, SessionRead, MessageRead, ChatRequest


chat_router = APIRouter()


def get_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> Chat:
    return Chat(session)

def get_service(repo: Annotated[Chat, Depends(get_repo)]) -> ChatService:
    return ChatService(repo)


RepoDep = Annotated[Chat, Depends(get_repo)]
ServiceDep = Annotated[ChatService, Depends(get_service)]


@chat_router.post("/sessions", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: SessionCreate, repo: RepoDep):
    return await repo.create_session(title=payload.title)

@chat_router.get("/sessions", response_model=list[SessionRead])
async def list_sessions(repo: RepoDep):
    return await repo.get_sessions()

@chat_router.get("/sessions/{session_id}/messages", response_model=list[MessageRead])
async def get_chat_history(session_id: int, repo: RepoDep):
    return await repo.get_history(session_id)

@chat_router.post("/chat/{session_id}")
async def chat(session_id: int, payload: ChatRequest, service: ServiceDep):
    return StreamingResponse(
        service.generate_stream(session_id, payload.prompt),
        media_type="text/plain"
    )
