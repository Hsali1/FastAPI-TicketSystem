from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    image_file: str | None
    image_path: str


class TicketBase(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5)


class TicketCreate(TicketBase):
    created_by_id: int #temp


class TicketResponse(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime

    created_by_id: int
    assigned_to_id: int | None

    created_by: UserResponse
    assigned_to: UserResponse | None