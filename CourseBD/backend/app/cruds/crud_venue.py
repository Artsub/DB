from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.oauth2 import get_current_user
from app.models import Venue, User

# Создание площадки (только для администратора)
async def create_venue(db: AsyncSession, venue_data: dict,current_user: User):
    if current_user.role_id != 1:  # Проверка роли (1 - администратор)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    db_venue = Venue(**venue_data)
    db.add(db_venue)
    await db.commit()
    await db.refresh(db_venue)
    return db_venue


async def get_venue(db: AsyncSession, venue_id: int, current_user: User):
    result = await db.execute(select(Venue).filter_by(id=venue_id))
    venue = result.scalars().first()
    if venue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Venue with ID {venue_id} not found")
    return venue

async def get_all_venues(db: AsyncSession, current_user: User):
    result = await db.execute(select(Venue))
    return result.scalars().all()

