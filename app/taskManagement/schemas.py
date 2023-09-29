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