from app.models.ticket import Ticket
from app.services.ai_service import analyze_ticket
from app.database import get_db,SessionLocal
from app.models.user import User
from app.dependencies import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,BackgroundTasks

router = APIRouter()

@router.post('/tickets')
def create_ticket(title:str, description:str,
                  background_tasks: BackgroundTasks,
                  db:Session=Depends(get_db),
                  current_user:User = Depends(get_current_user)):
    ticket=Ticket(title=title,description=description,user_id=current_user.id)
    db.add(ticket)
    db.commit()
    background_tasks.add_task(analyze_and_update,ticket.id)

    return ticket

def analyze_and_update(ticket_id=int):
    db=SessionLocal()
    ticket=db.query(Ticket).filter(Ticket.id == ticket_id).first()
    result=analyze_ticket(ticket.description)

    ticket.category=result.category
    ticket.priority=result.priority
    db.commit()
    db.close()