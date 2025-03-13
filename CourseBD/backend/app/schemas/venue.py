from pydantic import BaseModel, field_validator, ValidationError

class VenueCreate(BaseModel):
    name: str
    address: str
    capacity: int

    @field_validator("capacity")
    def check_capacity_not_zero(cls, value):
        if value == 0:
            raise ValueError("Capacity must not be equal to 0")
        return value

class VenueResponse(VenueCreate):
    id: int

class VenueUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    capacity: int | None = None