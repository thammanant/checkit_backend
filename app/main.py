from fastapi import FastAPI
from taskManagement import models
from taskManagement.database import engine
from taskManagement.routers import user, task, team, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(team.router)
