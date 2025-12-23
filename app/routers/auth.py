from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from app import config
from jose import jwt

'''Why passlib not haslib : more secure '''
router = APIRouter()
# psw_context = CryptContext(schemes=["bcrypt"])


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long (max 72 bytes)")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    print(len(password))
    hashed_psw = hash_password(password)
    user = User(email=email, password_hash=hashed_psw)
    db.add(user)
    db.commit()
    return {"message": "user registered"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = jwt.encode({"user_id": user.id}, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return {"access_token": token}
