from fastapi import APIRouter
from taskManagement import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from taskManagement.services import team

router = APIRouter(
    prefix="/user/team",
    tags=['Teams']
)

get_db = database.getDB

# Team/create
@router.post("/create", status_code=status.HTTP_201_CREATED)
def createTeam(request: schemas.Team, db: Session = Depends(get_db)):
    return team.createTeam(request, db)

# Team/editName
# edit Team using query parameters
@router.put("/editName", status_code=status.HTTP_202_ACCEPTED)
def editTeam(team_id: int, request: schemas.Team, db: Session = Depends(get_db)):
    return team.editTeam(team_id, request, db)

# Team/addTask
# add Task to Team using query parameters
@router.put("/addTask", status_code=status.HTTP_202_ACCEPTED)
def addTaskToTeam(team_id: int, task_id: int, db: Session = Depends(get_db)):
    return team.addTaskToTeam(team_id, task_id, db)

# Team/addUser
# add User to Team using query parameters
@router.put("/addUser", status_code=status.HTTP_202_ACCEPTED)
def addUserToTeam(team_id: int, email: str, db: Session = Depends(get_db)):
    return team.addUserToTeam(team_id, email, db)

# Team/removeUser
# remove User from Team using query parameters
@router.put("/removeUser", status_code=status.HTTP_202_ACCEPTED)
def removeUserFromTeam(team_id: int, email: str, db: Session = Depends(get_db)):
    return team.removeUserFromTeam(team_id, email, db)

# Team/removeTask
# remove Task from Team using query parameters
@router.put("/removeTask", status_code=status.HTTP_202_ACCEPTED)
def removeTaskFromTeam(team_id: int, task_id: int, db: Session = Depends(get_db)):
    return team.removeTaskFromTeam(team_id, task_id, db)


# Team/delete
# delete Team using query parameters
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def deleteTeam(team_id: int, db: Session = Depends(get_db)):
    return team.deleteTeam(team_id, db)

# Team/getAllTeams
@router.get("/getAllTeams", status_code=status.HTTP_200_OK)
def getAllTeams(db: Session = Depends(get_db)):
    return team.getAllTeams(db)

# Team/getTeamTasks
# get all Tasks associated with a Team using query parameters
@router.get("/getTeamTasks", status_code=status.HTTP_200_OK)
def getAllTasksForTeam(team_id: int, db: Session = Depends(get_db)):
    return team.getAllTasksForTeam(team_id, db)

# Team/getTeamUsers
# get all Users associated with a Team using query parameters
@router.get("/getTeamUsers", status_code=status.HTTP_200_OK)
def getAllUsersForTeam(team_id: int, db: Session = Depends(get_db)):
    return team.getAllUsersForTeam(team_id, db)

# Team/getTeamUsersStatus
# TODO

