from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int