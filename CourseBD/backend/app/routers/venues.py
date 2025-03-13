from fastapi import APIRouter, Depends, HTTPException, Body, responses, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.oauth2 import get_current_user
from ..database import get_db
from ..models import User, Venue
from sqlalchemy.future import select
from ..schemas.venue import VenueCreate, VenueResponse, VenueUpdate
from ..cruds import crud_venue

router = APIRouter(prefix="/venues", tags=["Venues"])

@router.post("/", response_model=VenueResponse)
async def create_venue(
    venue: VenueCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crud_venue.create_venue(db, venue.model_dump(), current_user)

@router.get("/{venue_id}")
async def read_venue(venue_id: int, db: AsyncSession = Depends(get_db),  current_user: User = Depends(get_current_user)):
    return await crud_venue.get_venue(db, venue_id, current_user)

@router.get("/", response_model=list[VenueResponse])
async def read_all_venues(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_venue.get_all_venues(db, current_user)

@router.put("/{venue_id}", response_model=VenueCreate)
async def update_venue(venue_id: int, venue_data: VenueUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")

    result = await db.execute(select(Venue).filter_by(id=venue_id))
    venue = result.scalars().first()

    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Venue with ID {venue_id} not found")

    for key, value in venue_data.model_dump(exclude_unset=True).items():
        setattr(venue, key, value)

    await db.commit()
    await db.refresh(venue)
    return venue

# Удаление площадки (DELETE, только администратор)
@router.delete("/{venue_id}")
async def delete_venue(venue_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")

    result = await db.execute(select(Venue).filter_by(id=venue_id))
    venue = result.scalars().first()

    if not venue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Venue with ID {venue_id} not found")

    await db.delete(venue)
    await db.commit()
    return {"message": f"Venue {venue_id} deleted successfully"}