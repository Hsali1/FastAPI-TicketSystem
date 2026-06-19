from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5, max_length=500)

