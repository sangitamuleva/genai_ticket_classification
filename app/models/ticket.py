from sqlalchemy import Column,Integer,ForeignKey,String,Text,Enum
from app.database import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    title = Column(String(255))
    description = Column(Text)
    category = Column(String(255))
    priority = Column(Enum("low","medium","high"))
    status = Column(Enum('open',"closed"))