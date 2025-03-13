from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import app.database as database, app.schema as schema, app.models as models, app.utils as utils, app.oauth2 as oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print("testing")
    try:
        user = db.query(models.User).filter(
            models.User.email == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
        
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        #create token 
        access_token = oauth2.create_access_token(data = {"user_id" : user.id})
        return {"access_token" : access_token, "token_type": "bearer"}  

    except Exception as e:
        print(f"Error is {e}")