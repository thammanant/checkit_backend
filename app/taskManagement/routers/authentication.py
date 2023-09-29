from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from taskManagement import schemas, models, database, token
from taskManagement.encrypting import Encrypting
from taskManagement.services import user

router = APIRouter(tags=['Authentication'])

# validate user
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDB)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
    if not Encrypting.checkEncryptedPassword(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')
    
    access_token = token.createAccessToken(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# register user using createUser function from user.py
@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(request: schemas.User, db: Session = Depends(database.getDB)):
    return user.createUser(request, db)