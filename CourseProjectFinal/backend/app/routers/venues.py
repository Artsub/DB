from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.venue import VenueCreate, VenueResponse  # Убедитесь, что импортируете правильные схемы
from ..crud import *
from .. import crud

router = APIRouter(prefix="/venues", tags=["Venues"])

@router.post("/", response_model=VenueResponse)
async def create_venue(
    venue: VenueCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_venue(db, venue.model_dump())

@router.get("/{venue_id}", response_model=VenueResponse)
async def read_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    venue = await crud.get_venue(db, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.get("/", response_model=list[VenueResponse])
async def read_all_venues(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_venues(db)
