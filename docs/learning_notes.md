![alt text](user-ticket-rel.png)

1) A user can create an own many tickets, so we know our attribute Tickets can be a list of Tickets. But a Ticket can have only 1 creater so its type of just User. Now since we are using Python, if Hassan.created_tickets has a ticket with id 2, then Ticket_id_2_object.author MUST EQUAL Hassan. I Think back_populates keyword is what connects this relationship and also allows SQLAlchemy to create/update this relationship when a new item is added

2) The foreign keys seem kind of over the place so I will work with an assumption. I am assuming Hassan.created_tickets is a list of Tickets but so is Hassan.assigned tickets so we have to make sure the tickets that are in hassan.created_tickets must be in the Ticket.created_by_id column.