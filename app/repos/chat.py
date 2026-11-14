from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.chat import Session, Message


class Chat:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_session(self, title: str) -> Session:

        new_session = Session(title=title)
        self.session.add(new_session)
        await self.session.flush()
        return new_session


    async def get_sessions(self) -> List[Session]:

        result = await self.session.execute(select(Session).order_by(Session.created_at.desc()))
        return result.scalars().all()


    async def get_session(self, session_id: int) -> Optional[Session]:
        return await self.session.get(Session, session_id)


    async def create_message(self, session_id: int, role: str, content: str) -> Message:

        msg = Message(session_id=session_id, role=role, content=content)
        self.session.add(msg)
        await self.session.flush()
        return msg


    async def get_history(self, session_id) -> List[Message]:

        result = await self.session.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.created_at.asc())
        )

        return result.scalars().all()
