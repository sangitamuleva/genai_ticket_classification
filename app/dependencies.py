from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from jose import jwt, JWTError
from app import config
from app.models.user import User

security=HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db)
                     ):
    token=credentials.credentials
    try:
        payload = jwt.decode(token,config.SECRET_KEY,algorithms=[config.ALGORITHM])
        user_id=payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")

    user=db.query(User).filter(User.id== user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user