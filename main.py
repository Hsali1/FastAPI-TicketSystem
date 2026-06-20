from fastapi import FastAPI, Request, HTTPException, status
# My html forms were not giving Json with pydantic
from fastapi import Form 
# for HTML
from fastapi.templating import Jinja2Templates
# I want my endpoints to redirect to other ones
from fastapi.responses import RedirectResponse 
# Exceptions
    ## handles errors like when input is "hello" when expecting int
from fastapi.exceptions import RequestValidationError
    ## manually return Json responses from exception handler
from fastapi.responses import JSONResponse
    ## When user goes to a route that doesn't exist
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas.schemas import TicketCreate, TicketResponse


app = FastAPI()

templates = Jinja2Templates(directory="templates")

tickets = [
    {
        "id": 1,
        "author": "Hassan",
        "title": "Can't login to Epic",
        "description": "User unable to login after password reset.",
        "date_posted": "April 20, 2025",
        "status": "Open"
    },
    {
        "id": 2,
        "author": "Ali",
        "title": "Termination Ticket",
        "description": "Disable all access for departing employee.",
        "date_posted": "April 20, 2025",
        "status": "Open"
    }
]


@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/tickets", response_model=list[TicketResponse])
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
    description: str = Form(...),
    author: str = Form(...)
):
    new_id = max(tic["id"] for tic in tickets) + 1 if tickets else 1
    new_ticket = {
        "id": new_id,
        "author": author,
        "title": title,
        "description": description,
        "date_posted": "dummy date o clock",
        "status": "Open"
    }
    tickets.append(new_ticket)
    return RedirectResponse(
        url=f"/tickets/{new_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/tickets/{ticket_id}", response_model=TicketCreate)
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


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message
        },
        status_code=exception.status_code
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again."
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )