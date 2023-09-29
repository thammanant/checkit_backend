from fastapi import APIRouter
from taskManagement import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# User/editProfile
@router.put('/editProfile', status_code=status.HTTP_202_ACCEPTED)
def editProfile(email: str, request: schemas.User, db: Session = Depends(get_db)):
    return database.user.editUser(email, request, db)

# User/deleteProfile
@router.delete('/deleteProfile', status_code=status.HTTP_202_ACCEPTED)
def deleteProfile(email: str, db: Session = Depends(get_db)):
    return database.user.deleteUser(email, db)

# User/profile
@router.get('/profile', response_model=schemas.User)
def profile(email: str, db: Session = Depends(get_db)):
    return database.user.getUserByEmail(email, db)