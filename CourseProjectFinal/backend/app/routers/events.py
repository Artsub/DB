from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import get_all_events, create_event
from ..database import get_db
from ..schemas.event import EventResponse, EventCreate  # Убедитесь, что импортируете правильные схемы
from .. import crud
from ..schemas.event import EventResponse

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=list[dict])  # Указываем, что возвращаем список словарей
async def read_events(db: AsyncSession = Depends(get_db)):
    return await get_all_events(db)

@router.post("/")
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_event(
        db=db,
        title=event.title,
        description=event.description,
        date=event.date.isoformat(),
        venue_name=event.venue_name,
        category_name=event.category_name
    )