from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as sf:
        try:
            yield sf
            await sf.commit()
        except:
            await sf.rollback()
            raise