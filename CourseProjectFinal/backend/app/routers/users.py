from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.oauth2 import get_current_user
from ..database import get_db
from ..models import User
from ..schemas.user import UserResponse  # Убедитесь, что импортируете правильные схемы
from ..cruds import crud_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await crud_user.get_user(db, username, current_user)
    return user

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = await crud_user.get_users(db, current_user )
    return users

@router.delete("/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await crud_user.delete_user_by_id(db, id, current_user)
    return user

@router.patch("/{id}")
async def update_user(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = await crud_user.update_user_by_id(db, id, current_user)
    return user

