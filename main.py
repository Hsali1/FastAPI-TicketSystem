from pydoc import describe

from fastapi import FastAPI, Request, HTTPException, status, Depends
# My html forms were not giving Json with pydantic
from fastapi import Form 
# for HTML
from fastapi.staticfiles import StaticFiles
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

from typing import Annotated
# database support
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

from schemas.schemas import TicketCreate, TicketResponse, UserResponse, UserCreate

# Create database tables
"""
This looks at all of our models that inherit from Base
and creates the tables if they dont already exist
    - safe to run multiple times
"""
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


@app.get("/", include_in_schema=False, name="home")
@app.get("/tickets", include_in_schema=False, name="tickets")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Ticket))
    tickets = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"tickets": tickets, "title": "Home"}
    )


@app.get("/tickets/{ticket_id}", include_in_schema=False)
def get_ticket_page(request: Request, ticket_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Ticket).where(models.Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if ticket:
        title = ticket.title[:50]
        return templates.TemplateResponse(
            request,
            "ticket.html",
            {"ticket": ticket, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


# tickets created by user
@app.get("/users/{user_id}/created_tickets", include_in_schema=False, name="user_created_tickets_page")
def user_created_tickets_page(request: Request, user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    result = db.execute(select(models.Ticket).where(models.Ticket.created_by_id == user_id))
    tickets = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_tickets.html",
        {"tickets": tickets, "user": user, "title": f"{user.username}'s Created Tickets"}
    )


# tickets assigned to user
@app.get("/users/{user_id}/assigned_tickets", include_in_schema=False, name="user_assigned_tickets_page")
def user_assigned_tickets_page(request: Request, user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    result = db.execute(select(models.Ticket).where(models.Ticket.assigned_to_id == user_id))
    tickets = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_tickets.html",
        {"tickets": tickets, "user": user, "title": f"{user.username}'s Assigned Tickets"}
    )


@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):

    # make sure username does not exist
    result = db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # make sure email does not exist
    result = db.execute(select(models.User).where(models.User.email == user.email))
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_user = models.User(
        username=user.username,
        email=user.email
    )

    db.add(new_user) # stages insert
    db.commit() # executes insert
    db.refresh(new_user) # reloads object from database

    return new_user
    

@app.get("/api/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if user:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# get all tickets created by a user (api version)
@app.get("/api/users/{user_id}/tickets_created", response_model=list[TicketResponse])
def get_user_created_tickets(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    result = db.execute(select(models.Ticket).where(models.Ticket.created_by_id == user_id))
    tickets = result.scalars().all()
    return tickets


# get all tickets assigned to a user (api version)
@app.get("/api/users/{user_id}/tickets_assigned", response_model=list[TicketResponse])
def get_user_assigned_tickets(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    result = db.execute(select(models.Ticket).where(models.Ticket.assigned_to_id == user_id))
    tickets = result.scalars().all()
    return tickets


@app.get("/api/tickets", response_model=list[TicketResponse])
def get_tickets_api(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Ticket))
    tickets = result.scalars().all()
    return tickets


@app.post(
        "/api/tickets",
        response_model=TicketResponse,
        status_code=status.HTTP_201_CREATED
)
def create_ticket_api(ticket: TicketCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == ticket.created_by_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        created_by_id=ticket.created_by_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket_api(ticket_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Ticket).where(models.Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if ticket:
        return ticket
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


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