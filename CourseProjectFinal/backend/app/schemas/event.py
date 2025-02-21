from pydantic import BaseModel
from datetime import datetime
from typing import List

class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    venue_name: str
    category_name: str

class EventResponse(EventCreate):
     id: int
