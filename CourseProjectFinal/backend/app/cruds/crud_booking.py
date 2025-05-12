from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from app.auth.oauth2 import get_current_user
from app.models import Booking, User

# Получение всех бронирований (только для администратора)
async def get_all_bookings(db: AsyncSession, current_user: User):
    if current_user.role_id != 1:  # Проверка роли (1 - администратор)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    query = text("SELECT * FROM get_bookings()")
    result = await db.execute(query)
    return result.mappings().all()

# Получение бронирований по имени пользователя (доступно администратору или самому пользователю)
async def get_booking(db: AsyncSession, username: str, current_user: User):
    if current_user.role_id != 1 and current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    query = text("SELECT * FROM get_bookings_by_username(:username)")
    result = await db.execute(query, {"username": username})
    return result.mappings().all()


async def create_booking(db: AsyncSession, booking_data: dict, current_user: User):
    booking_data["user_id"] = current_user.id
    if booking_data["booking_date"].tzinfo is not None:
        booking_data["booking_date"] = booking_data["booking_date"].replace(tzinfo=None)
    db_booking = Booking(**booking_data)
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

# Удаление бронирования (доступно администратору или самому пользователю)
async def delete_booking(db: AsyncSession, booking_id: int, current_user: User):
    result = await db.execute(select(Booking).filter_by(id=booking_id))
    booking = result.scalars().first()
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    if current_user.role_id != 1 and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this booking"
        )
    await db.delete(booking)
    await db.commit()
    return {"message": "Booking deleted successfully"}

async def update_booking(db: AsyncSession, booking_id: int, current_user: User):
    result = await db.execute(select(Booking).filter_by(id=booking_id))
    booking = result.scalars().first()

    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {booking_id} not found")

    if current_user.role_id != 1 and booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )

    if not booking.payment_status:
        booking.payment_status = True

    # Сохранение изменений в базе данных
    await db.commit()
    await db.refresh(booking)

    return {"message": f"Booking {booking_id} status updated"}