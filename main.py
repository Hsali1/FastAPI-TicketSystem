from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

tickets = [
  {
    "id": 1,
    "title": "Can't login to Epic",
    "status": "Open"
  },
  {
    "id": 2,
    "title": "Termination Ticket",
    "status": "Open"
  }
]

@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/tickets")
def get_tickets(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"tickets": tickets})


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )