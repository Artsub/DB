from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.user import UserResponse  # Убедитесь, что импортируете правильные схемы
from ..crud import *
from .. import crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}", response_model=UserResponse)
async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

