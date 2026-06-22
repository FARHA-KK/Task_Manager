from fastapi import FastAPI

from database import init_db

from routers.users import router as user_router
from routers.tasks import router as task_router


app = FastAPI(
    title="Personal Task Manager"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {"message": "Task Manager API Running"}


app.include_router(user_router)
app.include_router(task_router)