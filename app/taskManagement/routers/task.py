from fastapi import APIRouter
from taskManagement import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/user/task",
    tags=['Tasks']
)

get_db = database.get_db

# Task/create
# create Task and append it to User
@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Task, email: str, db: Session = Depends(get_db)):
    task = database.task.create(request, db)
    database.task.appendTaskToUser(task.task_id, email, db)
    return task

# Task/edit
# edit Task using query parameter task_id
@router.put('/edit', status_code=status.HTTP_202_ACCEPTED)
def edit(task_id: int, request: schemas.Task, db: Session = Depends(get_db)):
    return database.task.edit(task_id, request, db)

# Task/delete
# delete Task using query parameter task_id
@router.delete('/delete', status_code=status.HTTP_202_ACCEPTED)
def delete(task_id: int, db: Session = Depends(get_db)):
    return database.task.delete(task_id, db)

