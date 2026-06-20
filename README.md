In progress...

## Goals 
- ~~Display tickets~~
- ~~Get ticket by ID~~
- ~~Allow creation of tickets through forms~~
- Introduce persistent store with SQLAlchemy
- Introduce users and authentication (Password hashing, authentication, etc)
- Introduce roles? customers/analysts (Authorization, permissions, etc)
- Ticket comments (analysts document their work so others can see)
- Teams (tickets getting assigned to specific teams so analysts can see/work)


## Notes
For database and permissions I am thinking:

### Customer permissions

#### Customer can:

- Create ticket
- View all tickets
- View ticket details
- Add comments to tickets

#### Customer cannot:

- Assign tickets
- Change status
- Delete tickets
- Edit tickets

### Analyst permissions

#### Analyst can:

- Everything customer can do
- Assign ticket to self
- Change status
- Add work notes
- Close ticket