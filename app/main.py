from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.dialects.oracle.dictionary import all_users
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=schemas.User)
async def get_all_users(db: Session = Depends(get_db)):
    try:
        all_users = crud.get_users(db)
        if all_users is None:
            return {
                "message": "There is no user yet"
            }
        else:
            return {
                "Users": all_users
            }
    except Exception as e:
        return {
            "Error": e
        }