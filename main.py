from fastapi import FastAPI, Request, HTTPException, status
from fastapi import Form # My html forms were not giving Json with pydantic
from fastapi.templating import Jinja2Templates

from fastapi.responses import RedirectResponse # I want my endpoints to redirect to other ones

from schemas.schemas import TicketCreate

app = FastAPI()

templates = Jinja2Templates(directory="templates")

tickets = [
    {
        "id": 1,
        "title": "Can't login to Epic",
        "description": "User unable to login after password reset.",
        "status": "Open"
    },
    {
        "id": 2,
        "title": "Termination Ticket",
        "description": "Disable all access for departing employee.",
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


@app.get("/tickets/new")
def new_ticket_form(request: Request):
    return templates.TemplateResponse(
        request,
        "create_ticket.html"
    )

@app.post("/tickets/new")
def new_ticket_submit(
    title: str = Form(...),
    description: str = Form(...)
):
    new_id = max(tic["id"] for tic in tickets) + 1 if tickets else 1
    new_ticket = {
        "id": new_id,
        "title": title,
        "description": description,
        "status": "Open"
    }
    tickets.append(new_ticket)
    return RedirectResponse(
        url=f"/tickets/{new_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, request: Request):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return templates.TemplateResponse(
                request,
                "ticket.html",
                {"ticket": ticket}
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )


@app.post("/tickets")
def create_ticket(ticket: TicketCreate):
    new_id = max(tic["id"] for tic in tickets) + 1 if tickets else 1
    new_ticket = {
        "id": new_id,
        "title": ticket.title,
        "description": ticket.description,
        "status": "Open"
    }
    tickets.append(new_ticket)
    return new_ticket
