from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str