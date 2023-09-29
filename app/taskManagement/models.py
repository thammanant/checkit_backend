from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from taskManagement.database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)

    tasks = relationship('Task', secondary='user_tasks', back_populates='users')
    teams = relationship('TeamUser', back_populates='user')

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    priority = Column(String)
    category = Column(String)
    status = Column(String)

    users = relationship('User', secondary='user_tasks', back_populates='tasks')
    categories = relationship('TaskCategory', back_populates='task')
    teams = relationship('TeamTask', back_populates='task')

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner = Column(String)

    users = relationship('TeamUser', back_populates='team')
    tasks = relationship('TeamTask', back_populates='team')

class UserTask(Base):
    __tablename__ = "user_tasks"

    email = Column(String, ForeignKey("users.email"), primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True, index=True)

class TaskCategory(Base):
    __tablename__ = "task_categories"

    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True, index=True)
    category = Column(String, primary_key=True, index=True)

    task = relationship('Task', back_populates='categories')

class TeamUserStatus(Base):
    __tablename__ = "team_userstatus"

    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"), primary_key=True, index=True)
    user_status = Column(String)

class TeamTask(Base):
    __tablename__ = "team_tasks"

    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True, index=True)

    team = relationship('Team', back_populates='tasks')
    task = relationship('Task', back_populates='teams')

class TeamUser(Base):
    __tablename__ = "team_users"

    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"), primary_key=True, index=True)

    team = relationship('Team', back_populates='users')
    user = relationship('User', back_populates='teams')