from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.dialects.oracle.dictionary import all_users
from sqlalchemy.orm import Session

from . import crud, models, schemas, common
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


@app.get("/users/")
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


@app.get("/")
async def main():
    try:
        return {
            "message": "welcome to my apps"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db) ):
    get_user = crud.get_user_by_email(db, user_email = user.email)

    check_email = common.check_email_format(user.email)

    if not check_email:
        raise HTTPException(status_code=400, detail="Email format is not valid")

    if not get_user:
        user = crud.create_user(db, user = user)
        return {
            "message": user
        }
    raise HTTPException(status_code=400, detail="Email already registered")
    


@app.get("/search_user_by_email/", response_model=schemas.User)
async def search_user_by_email(user: schemas.UserBase, db: Session = Depends(get_db)):
    user_email = crud.get_user_by_email(db, user_email=user.email)
    if user_email:
        return{"Message": user_email}
    else:
        raise HTTPException(status_code=400, detail="Email does not exist")
