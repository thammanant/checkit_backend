from sqlalchemy.orm import Session
from taskManagement import models, schemas
from fastapi import HTTPException, status
from random import randint


# create Team
def createTeam(request: schemas.Team, db: Session):
    new_team = models.Team(
        name=request.name,
        owner=request.owner,
    )
    
    # Associate the team with the user using the TeamUser association table
    user = db.query(models.User).filter(models.User.email == request.owner).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {request.owner} not found")
    
    # Generate a random team_id
    new_team.team_id = randint(1000, 9999)
    # check if the generated team_id already exists
    while db.query(models.Team).filter(models.Team.team_id == new_team.team_id).first():
        new_team.team_id = randint(1000, 9999)
        
    team_user_association = models.TeamUser(team_id=new_team.team_id, email=request.owner)
    db.add(new_team)
    db.add(team_user_association)
    db.commit()
    return 'created'
    
    
# edit Team name
def editTeam(team_id: int, request: schemas.Team, db: Session):
    try:
        team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
        
        # Convert the Pydantic model to a dictionary
        update_data = request.dict(exclude_unset=True)
        
        # Update team attributes
        for key, value in update_data.items():
            setattr(team, key, value)
        
        db.commit()
        return 'updated'
    
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e
    
# add Team user status
# TODO
    
# add Task to Team
def addTaskToTeam(team_id: int, task_id: int, db: Session):
    try:
        team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
        task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
        
        # Associate the task with the team using the TeamTask association table
        team_task_association = models.TeamTask(team_id=team_id, task_id=task_id)
        db.add(team_task_association)
        
        # Update the task status to 'In Progress'
        task.status = 'In Progress'
        
        db.commit()
        return 'updated'
    
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e

# add User to Team
def addUserToTeam(team_id: int, email: str, db: Session):
    try:
        team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
        user = db.query(models.User).filter(models.User.email == email).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
        
        # Associate the user with the team using the TeamUser association table
        team_user_association = models.TeamUser(team_id=team_id, email=email)
        db.add(team_user_association)
        
        # Associate the user with the team using the TeamUserStatus association table
        team_user_status_association = models.TeamUserStatus(team_id=team_id, email=email, user_status='Active')
        db.add(team_user_status_association)
        
        db.commit()
        return 'updated'
    
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e

# remove Task from Team
def removeTaskFromTeam(team_id: int, task_id: int, db: Session):
    try:
        team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
        task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
        
        # Remove the task from the team using the TeamTask association table
        db.query(models.TeamTask).filter(models.TeamTask.team_id == team_id).filter(models.TeamTask.task_id == task_id).delete(synchronize_session=False)
        
        # Update the task status to 'Pending'
        task.status = 'Pending'
        
        db.commit()
        return 'updated'
    
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e
    
# remove User from Team
def removeUserFromTeam(team_id: int, email: str, db: Session):
    try:
        team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
        user = db.query(models.User).filter(models.User.email == email).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
        
        # Remove the user from the team using the TeamUser association table
        db.query(models.TeamUser).filter(models.TeamUser.team_id == team_id).filter(models.TeamUser.email == email).delete(synchronize_session=False)
        
        # Remove the user from the team using the TeamUserStatus association table
        db.query(models.TeamUserStatus).filter(models.TeamUserStatus.team_id == team_id).filter(models.TeamUserStatus.email == email).delete(synchronize_session=False)
        
        db.commit()
        return 'updated'
    
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e

# delete Team
# delete Team from all the association tables
def deleteTeam(team_id: int, db: Session):
    # Get the team and associated user associations
    team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    
    # Delete associated team_user associations
    db.query(models.TeamUser).filter(models.TeamUser.team_id == team_id).delete(synchronize_session=False)
    
    # Delete associated team_task associations
    db.query(models.TeamTask).filter(models.TeamTask.team_id == team_id).delete(synchronize_session=False)
    
    # Delete associated team_userstatus associations
    db.query(models.TeamUserStatus).filter(models.TeamUserStatus.team_id == team_id).delete(synchronize_session=False)
    
    # Delete the team
    db.delete(team)
    db.commit()
    
    return 'deleted'

# get all Teams
def getAllTeams(db: Session):
    teams = db.query(models.Team).all()
    return teams

# get all Tasks for a Team
def getAllTasksForTeam(team_id: int, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    tasks = db.query(models.Task).join(models.TeamTask).filter(models.TeamTask.team_id == team_id).all()
    return tasks

# get all Users for a Team
def getAllUsersForTeam(team_id: int, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    users = db.query(models.User).join(models.TeamUser).filter(models.TeamUser.team_id == team_id).all()
    return users

# get all Users for a Team with their status
def getAllUsersForTeamWithStatus(team_id: int, db: Session):
    team = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    users = db.query(models.User).join(models.TeamUser).join(models.TeamUserStatus).filter(models.TeamUser.team_id == team_id).all()
    return users
