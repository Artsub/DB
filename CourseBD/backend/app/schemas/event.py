from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List

class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    venue_name: str
    category_name: str

    @field_validator("date")
    def remove_timezone(cls, value):
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value

class EventResponse(EventCreate):
     id: int
