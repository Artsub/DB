from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.crud import get_user, create_user
from app.auth.hash_password import HashPassword
from app.schemas.user import UserCreate, UserResponse
from . import oauth2


router = APIRouter(
    tags=['authentication'],
)


@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user(db, username=request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not HashPassword.verify(user.password_hash, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')

    access_token = oauth2.create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user_data.username,  user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user