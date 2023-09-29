from fastapi import APIRouter
from taskManagement import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/user/team",
    tags=['Teams']
)

get_db = database.getDB

# Team/create
# create Team and set Owner of Team and append Team to User
@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Team, email: str, db: Session = Depends(get_db)):
    team = database.team.create(request, db)
    database.team.setOwner(team.team_id, email, db)
    return team

# Team/addUser
# append User to Team
@router.put('/addUser', status_code=status.HTTP_202_ACCEPTED)
def addUser(team_id: int, email: str, db: Session = Depends(get_db)):
    return database.team.appendUser(team_id, email, db)

# Team/edit
# edit Team using query parameter team_id
@router.put('/edit', status_code=status.HTTP_202_ACCEPTED)
def edit(team_id: int, request: schemas.Team, db: Session = Depends(get_db)):
    return database.team.edit(team_id, request, db)

# Team/delete
# delete Team using query parameter team_id
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED)
def delete(team_id: int, db: Session = Depends(get_db)):
    return database.team.delete(team_id, db)

# Team/createTask
# create Task and append it to Team
@router.post('/createTask', status_code=status.HTTP_201_CREATED)
def createTask(request: schemas.Task, team_id: int, db: Session = Depends(get_db)):
    task = database.task.create(request, db)
    database.task.appendTaskToTeam(task.task_id, team_id, db)
    return task

# Team/removeTask
# remove Task from Team
@router.put('/removeTask', status_code=status.HTTP_202_ACCEPTED)
def removeTask(task_id: int, team_id: int, db: Session = Depends(get_db)):
    return database.task.removeTaskFromTeam(task_id, team_id, db)

# Team/editTask
# edit Task using query parameter task_id
@router.put('/editTask', status_code=status.HTTP_202_ACCEPTED)
def editTask(task_id: int, request: schemas.Task, db: Session = Depends(get_db)):
    return database.task.editTask(task_id, request, db)


