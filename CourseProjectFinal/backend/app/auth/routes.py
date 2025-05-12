from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, RevokedToken  # Импортируем RevokedToken
from app.cruds.crud_user import get_user_by_username, create_user
from app.auth.hash_password import HashPassword
from app.schemas.user import UserCreate, UserResponse
from . import oauth2

router = APIRouter(tags=['authentication'])

@router.post('/token')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, username=request.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    if not HashPassword.verify(user.password_hash, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong password')

    access_token = oauth2.create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username,
        'role_id': user.role_id
    }

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user

@router.post("/logout")
async def logout(token: str = Depends(oauth2.oauth2_schema), db: AsyncSession = Depends(get_db)):
    # Создаем объект RevokedToken
    db_revoked_token = RevokedToken(token=token)
    db.add(db_revoked_token)
    await db.commit()
    return {"message": "Successfully logged out"}