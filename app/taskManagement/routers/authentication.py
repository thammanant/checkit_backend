from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from taskManagement import schemas, models, database, token
from taskManagement.encrypting import Encrypting

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.getDB)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    
    if not Encrypting.checkEncryptedPassword(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')
    
    access_token = token.createAccessToken(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}