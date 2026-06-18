from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=200)