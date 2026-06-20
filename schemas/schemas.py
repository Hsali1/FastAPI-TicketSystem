from pydantic import BaseModel, Field, ConfigDict

class TicketBase(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=5)
    author: str = Field(min_length=1, max_length=50)


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    date_posted: str