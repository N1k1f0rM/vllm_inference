from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.repos.user import UserRepo
from app.schemas.models import User


router = APIRouter(prefix="/users", tags=["tags"])


def get_user_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepo:
    return UserRepo(session)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    repo: Annotated[AsyncSession, Depends(get_user_repo)]
):
    return await repo.create()