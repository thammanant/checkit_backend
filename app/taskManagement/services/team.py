from sqlalchemy.orm import Session
from taskManagement import models, schemas
from fastapi import HTTPException, status
from random import randint

# create Team
def create(request: schemas.Team, db: Session):
    new_team = models.Team(
        name=request.name,
        user_list=request.user_list,
        user_status=request.user_status,
        taskList=request.taskList,
        owner=request.owner,
    )
    # generate team_id with 4 digits
    new_team.team_id = randint(1000, 9999)
    
    # check if team_id already exists if so generate new team_id
    team = db.query(models.Team).filter(models.Team.team_id == new_team.team_id).first()
    while team:
        new_team.team_id = randint(1000, 9999)
        team = db.query(models.Team).filter(models.Team.team_id == new_team.team_id).first()
        
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

# edit Team
def edit(team_id: int, request: schemas.Team, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    team.update(request)
    db.commit()
    return 'updated'

# delete Team
def delete(team_id: int, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    team.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

# set Owner of Team and append Team to User
def setOwner(team_id: int, email: str, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    user = db.query(models.User).filter(models.User.email == email)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    team.update({'owner': email})
    user.update({'teamList': user.first().teamList + [team_id]})
    db.commit()
    return 'updated'

# append User to Team
def appendUser(team_id: int, email: str, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    user = db.query(models.User).filter(models.User.email == email)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    team.update({'user_list': team.first().user_list + [email]})
    user.update({'teamList': user.first().teamList + [team_id]})
    db.commit()
    return 'updated'