from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Base class for Task
class TaskBase(BaseModel):
    title: str = Field(..., example="Task Title")
    description: Optional[str] = None
    start: datetime = Field(..., example="2021-01-01 00:00:00")
    end: datetime = Field(..., example="2021-01-01 00:00:00")
    priority: str = Field(..., example="High")
    category: str = Field(..., example="Work")
    status: bool = Field(..., example=True)
    task_id: int

class Task(TaskBase):    
    class Config():
        orm_mode = True

# Base class for Team
class TeamBase(BaseModel):
    name: str = Field(..., example="Team Name")
    user_list: Optional[List[str]] = []
    user_status: List[dict] = []
    taskList: List[Task] = []
    owner: str = Field(..., example="Owner Name")
    team_id: int

class Team(TeamBase):
    class Config():
        orm_mode = True

# Base class for User
class User(BaseModel):
    email: str = Field(..., example="example@gmail.com")
    name: str = Field(..., example="Name")
    password: str = Field(..., example="Password")
    taskList: List[Task] = []
    teamList: List[Team] = []
    
# ShowUser is used to show the user in the response
class ShowUser(User):
    email: str = Field(..., example="example@gmail.com")
    name: str = Field(..., example="Name")
    taskList: List[Task] = []
    teamList: List[Team] = []
    class Config():
        orm_mode = True


class Login(BaseModel):
    email: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None