from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Venue, Event, User, Role
from app.auth.hash_password import HashPassword
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, ProgrammingError


#круды для venue
async def create_venue(db: AsyncSession, venue_data: dict):
    db_venue = Venue(**venue_data)
    db.add(db_venue)
    await db.commit()
    await db.refresh(db_venue)
    return db_venue

async def get_venue(db: AsyncSession, venue_id: int):
    result = await db.execute(select(Venue).filter_by(id=venue_id))  # Используем filter_by вместо filter
    return result.scalar_one_or_none()

async def get_all_venues(db: AsyncSession):
    result = await db.execute(select(Venue))
    return result.scalars().all()

#круды для events
async def get_all_events(db: AsyncSession):
    query = text("SELECT * FROM get_events_with_sponsors()")
    result = await db.execute(query)
    return result.mappings().all()  # Используем mappings(), чтобы получить результат как список словарей


async def create_event(db: AsyncSession, title: str, description: str, date: str, venue_name: str, category_name: str):
    try:
        query = text("SELECT insert_event(:title, :description, :date, :venue_name, :category_name)")
        await db.execute(query, {
            "title": title,
            "description": description,
            "date": date,
            "venue_name": venue_name,
            "category_name": category_name
        })
        await db.commit()
        return {"message": f'Event "{title}" successfully created'}

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error: " + str(e.orig))

    except ProgrammingError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="SQL syntax error or function issue: " + str(e.orig))

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
#круды для user

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter_by(username=username))  # Используем filter_by вместо filter
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

async def create_user(db: AsyncSession, username: str, password: str):
    new_user = User(username=username,  password_hash=HashPassword.bcrypt(password), role_id = 1)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        return None