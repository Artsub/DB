from pydantic import BaseModel

class VenueCreate(BaseModel):
    name: str
    address: str
    capacity: int

class VenueResponse(VenueCreate):
    id: int
