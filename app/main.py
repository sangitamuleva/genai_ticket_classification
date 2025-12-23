from fastapi import FastAPI
from app.routers import auth,ticket
from app.database import engine,Base
from app.models.user import User
from app.models.ticket import Ticket

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router,prefix="/auth")
app.include_router(ticket.router)