from sqlalchemy.orm import Session
from taskManagement import models, schemas
from fastapi import HTTPException, status

# create Task
def createTask(request: schemas.Task, email: str, db: Session):
    # Create a new task object
    new_task = models.Task(
        title=request.title,
        description=request.description,
        start=request.start,
        end=request.end,
        priority=request.priority,
        category=request.category,
        status=request.status,
    )
    
    # Add the new task to the session and commit to the database
    db.add(new_task)
    db.commit()
    
    # Retrieve the newly generated task_id
    task_id = new_task.task_id
    
    # Associate the task with the user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")

    user_task_association = models.UserTask(email=email, task_id=task_id)
    db.add(user_task_association)
    db.commit()

    return 'created'


# edit Task
def editTask(task_id: int, request: schemas.Task, db: Session):
    try:
        task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")

        # Convert the Pydantic model to a dictionary
        update_data = request.dict(exclude_unset=True)

        # Update task attributes
        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        return 'updated'

    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise e


# delete Task
def deleteTask(task_id: int, db: Session):
    # Get the task and associated user_task associations
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    
    # Delete associated user_task associations
    db.query(models.UserTask).filter(models.UserTask.task_id == task_id).delete(synchronize_session=False)
    
    # Delete associated team_task associations
    db.query(models.TeamTask).filter(models.TeamTask.task_id == task_id).delete(synchronize_session=False)

    
    # Delete the task
    db.delete(task)
    db.commit()
    
    return 'deleted'

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

# get Task by task_id
def getTask(task_id: int, db: Session):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")
    return task

# get all Tasks
def getAllTasks(db: Session):
    tasks = db.query(models.Task).all()
    return tasks

# get all Tasks for a User
def getAllTasksForUser(email: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    tasks = db.query(models.Task).join(models.UserTask).filter(models.UserTask.email == email).all()
    return tasks
