from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User as UserModel


class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return await self.session.get(UserModel, user_id)


    async def create(self) -> UserModel:
        user = UserModel()
        self.session.add(user)
        await self.session.flush()
        return user