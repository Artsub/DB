from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.oauth2 import get_current_user
from ..cruds import crud_event
from ..database import get_db
from ..schemas.event import EventResponse, EventCreate
from ..cruds import crud_event
from ..schemas.event import EventResponse
from ..models import User

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/", response_model=list[dict])
async def read_events(db: AsyncSession = Depends(get_db)):
    return await crud_event.get_all_events(db)

@router.post("/", response_model=dict)
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud_event.create_event(db, event, current_user)
@router.get("/{event_id}")
async def read_events(event_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_event.get_event(event_id, db)

@router.delete("/{event_id}")
async def delete_events(event_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_event.delete_event(event_id, db, current_user)