# Database Design

## User ↔ Ticket Relationships

A ticket has two relationships to User:

- created_by
- assigned_to

The database stores:

Ticket.created_by_id
Ticket.assigned_to_id

SQLAlchemy exposes:

User.created_tickets
Ticket.created_by

User.assigned_tickets
Ticket.assigned_to

back_populates keeps both sides synchronized.