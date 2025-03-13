import app.models as models, app.schema as schema
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import engine, get_db
import app.models as models, app.schema as schema, app.utils as utils
from typing import List

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    #hash the passowrd - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user  = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model = schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id: {id} does not exist")
    return user
