from fastapi import APIRouter
from taskManagement import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from taskManagement.services import task

router = APIRouter(
    prefix="/user/task",
    tags=['Tasks']
)

get_db = database.getDB

# Task/create
# create Task and append it to User
@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, email: str, db: Session = Depends(get_db)):
    return task.createTask(request, email, db)

# Task/edit
# edit Task using query parameter task_id
@router.put('/edit', status_code=status.HTTP_202_ACCEPTED)
def edit(task_id: int, request: schemas.Task, db: Session = Depends(get_db)):
    return task.editTask(task_id, request, db)

# Task/delete
# delete Task using query parameter task_id
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED)
def delete(task_id: int, db: Session = Depends(get_db)):
    return task.deleteTask(task_id, db)

# Task/getTasks
# get Task using query parameter task_id
@router.get('/getTasks', status_code=status.HTTP_200_OK)
def getTasks(task_id: int, db: Session = Depends(get_db)):
    return task.getTask(task_id, db)

# Task/getAllTasks
# get all Tasks
@router.get('/getAllTasks', status_code=status.HTTP_200_OK)
def getAllTasks(db: Session = Depends(get_db)):
    return task.getAllTasks(db)

# get all Tasks for a User
@router.get('/getAllTasksForUser', status_code=status.HTTP_200_OK)
def getAllTasksForUser(email: str, db: Session = Depends(get_db)):
    return task.getAllTasksForUser(email, db)
