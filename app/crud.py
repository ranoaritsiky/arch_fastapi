from sqlalchemy.orm import Session
from . import schemas, models

def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db:Session, user: schemas.UserCreate):
    
    data_user = models.User(email=user.email, hashed_password=user.password)
    db.add(data_user)
    db.commit()
    db.refresh(data_user)
    return data_user

def get_users(db: Session):
    users =  db.query(models.User).all()
    return users


def get_user_by_email(db:Session, user_email:str):
    return db.query(models.User).filter(models.User.email == user_email).first()
