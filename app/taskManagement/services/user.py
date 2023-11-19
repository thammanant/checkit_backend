from sqlalchemy.orm import Session
from taskManagement import models, schemas
from fastapi import HTTPException, status
from taskManagement.encrypting import Encrypting


# create User
def createUser(request: schemas.User, db: Session):
    new_user = models.User(
        email=request.email,
        name=request.name,
        password=Encrypting.encryptPassword(request.password)
    )
    # check if email already exists
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email {request.email} already registered")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get User by email
def getUserByEmail(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    return user


# edit User
def editUser(email: str, request: schemas.User, db: Session):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

        # Convert the Pydantic model to a dictionary
        update_data = request.dict(exclude_unset=True)

        # Update user attributes
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        return 'updated'

    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e


# delete User
def deleteUser(email: str, db: Session):
    # Get the user and associated user_task and team_user associations
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    # Delete associated user_task associations
    db.query(models.UserTask).filter(models.UserTask.email == email).delete(synchronize_session=False)

    # Delete associated team_user associations
    db.query(models.TeamUser).filter(models.TeamUser.email == email).delete(synchronize_session=False)

    # Delete associated team_user_status associations
    db.query(models.TeamUserStatus).filter(models.TeamUserStatus.email == email).delete(synchronize_session=False)

    # Delete the user
    db.delete(user)
    db.commit()

    return 'deleted'


# get all teams of a user
def getTeamsOfUser(email: str, db: Session):
    # check if user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    # get all teams of user
    teams = db.query(models.Team).join(models.TeamUser).filter(models.TeamUser.email == email).all()
    return teams


# get all team pending status, return Team that have user as pending
def getTeamPendingStatus(email: str, db: Session):
    # check if user exists
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    # get all teams of user
    teams = db.query(models.Team).join(models.TeamUserStatus).filter(models.TeamUserStatus.email == email).filter(
        models.TeamUserStatus.user_status == 'pending').all()
    return teams
