from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    user_id: int
    event_id: int
    booking_date: datetime
    payment_status: bool = False