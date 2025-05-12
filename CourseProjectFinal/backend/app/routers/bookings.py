from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.oauth2 import get_current_user
from ..database import get_db
from ..cruds import crud_booking
from ..schemas.booking import BookingCreate
from ..models import User, Booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/")  # Указываем, что возвращаем список словарей
async def get_all_bookings(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_booking.get_all_bookings(db, current_user)

@router.get("/{username}")
async def get_booking(username: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_booking.get_booking(db, username, current_user)

@router.post("/")
async def post_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await crud_booking.create_booking(db, booking.model_dump() ,current_user)

@router.delete("/{booking_id}")
async def delete_booking(booking_id : int,db: AsyncSession = Depends(get_db),  current_user: User = Depends(get_current_user)):
    return await crud_booking.delete_booking(db, booking_id, current_user)

@router.patch("/{booking_id}")
async def update_booking(booking_id : int,db: AsyncSession = Depends(get_db),  current_user: User = Depends(get_current_user)):
    return await crud_booking.update_booking(db, booking_id, current_user)