from sqlalchemy.orm import Session
from taskManagement import models, schemas
from fastapi import HTTPException, status
from random import randint

# create Task
def createTask(request: schemas.Task, db: Session):
    new_task = models.Task(
        title=request.title,
        description=request.description,
        start=request.start,
        end=request.end,
        priority=request.priority,
        category=request.category,
        status=request.status,
    )
    # generate task_id with 6 digits
    new_task.task_id = randint(100000, 999999)
    
    # check if task_id already exists if so generate new task_id
    task = db.query(models.Task).filter(models.Task.task_id == new_task.task_id).first()
    while task:
        new_task.task_id = randint(100000, 999999)
        task = db.query(models.Task).filter(models.Task.task_id == new_task.task_id).first()
        
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# edit Task
def editTask(task_id: int, request: schemas.Task, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    task.update(request)
    db.commit()
    return 'updated'

# delete Task
def deleteTask(task_id: int, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    task.delete(synchronize_session=False)
    db.commit()
    return 'deleted'

# append Task to User
def appendTaskToUser(task_id: int, email: str, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id)
    user = db.query(models.User).filter(models.User.email == email)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    user.update({'taskList': user.first().taskList + [task_id]})
    db.commit()
    return 'updated'

# append Task to Team
def appendTaskToTeam(task_id: int, team_id: int, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id)
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    team.update({'taskList': team.first().taskList + [task_id]})
    db.commit()
    return 'updated'

# remove Task from Team
def removeTaskFromTeam(task_id: int, team_id: int, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id)
    team = db.query(models.Team).filter(models.Team.team_id == team_id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id {team_id} not found")
    team.update({'taskList': [task_id for task_id in team.first().taskList if task_id != task_id]})
    db.commit()
    return 'updated'
