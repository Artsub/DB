from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas.event import EventCreate
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, ProgrammingError
from app.auth.oauth2 import get_current_user
from app.models import Event, User

# Получение всех мероприятий (доступно всем)
async def get_all_events(db: AsyncSession):
    query = text("SELECT * FROM get_events_with_sponsors()")
    result = await db.execute(query)
    return result.mappings().all()

# Получение мероприятия по ID (доступно всем)
async def get_event(event_id: int, db: AsyncSession):
    query = text("SELECT * FROM get_event_by_id(:event_id)")
    result = await db.execute(query, {"event_id": event_id})
    return result.mappings().all()

# Создание мероприятия (только для администратора)
async def create_event(db: AsyncSession, event_data: EventCreate, current_user: User):
    # Проверка роли пользователя
    if current_user.role_id != 1:  # 1 - администратор
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )

    # Преобразуем datetime с временной зоной в datetime без временной зоны
    if event_data.date.tzinfo is not None:
        event_data.date = event_data.date.replace(tzinfo=None)

    try:
        # Выполняем SQL-запрос
        query = text("SELECT insert_event(:title, :description, :date, :venue_name, :category_name)")
        await db.execute(query, {
            "title": event_data.title,
            "description": event_data.description,
            "date": event_data.date,  # datetime без временной зоны
            "venue_name": event_data.venue_name,
            "category_name": event_data.category_name
        })
        await db.commit()
        return {"message": f'Event "{event_data.title}" successfully created'}

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error: " + str(e.orig))

    except ProgrammingError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="SQL syntax error or function issue: " + str(e.orig))

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

async def delete_event(event_id: int, db: AsyncSession, current_user: User):
    # Поиск события по ID
    if current_user.role_id != 1:  # 1 - администратор
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )

    result = await db.execute(select(Event).filter_by(id=event_id))
    event = result.scalars().first()

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found"
        )

    # Удаление события
    await db.delete(event)
    await db.commit()

    return {"message": f"Event {event_id} deleted successfully"}