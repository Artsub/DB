from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.oauth2 import get_current_user
from app.models import User
from app.auth.hash_password import HashPassword

# Получение пользователя по имени (только для администратора)
async def get_user(db: AsyncSession, username: str, current_user: User):
    if current_user.role_id != 1  and current_user.username != username:  # Проверка роли (1 - администратор)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    result = await db.execute(select(User).filter_by(username=username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with name {username} not found")
    return user

# Получение всех пользователей (только для администратора)
async def get_users(db: AsyncSession, current_user:  User = Depends(get_current_user)):
    if current_user.role_id != 1:  # Проверка роли (1 - администратор)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

# Создание пользователя (доступно всем)
async def create_user(db: AsyncSession, username: str, password: str):
    new_user = User(username=username, password_hash=HashPassword.bcrypt(password), role_id=2)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception:
        await db.rollback()
        return None

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter_by(username=username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with name {username} not found")
    return user

async def delete_user_by_id(db: AsyncSession, user_id: int, current_user: User):
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )

    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cant delete yourself"
        )
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    await db.delete(user)  # Удаляем пользователя
    await db.commit()  # Фиксируем изменения

    return {"message": f"User with ID {user_id} has been deleted"}

async def update_user_by_id(db: AsyncSession, user_id: int, current_user: User):
    if current_user.role_id != 1:  # Проверка роли (1 - администратор)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

    if user.role_id == 2:
        user.role_id = 1
    else:
        user.role_id = 2

    # Сохранение изменений в базе данных
    await db.commit()
    await db.refresh(user)

    return {"message": f"User {user_id} role updated to {user.role_id}"}