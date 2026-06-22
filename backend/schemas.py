from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str | None = None
class TaskStatusUpdate(BaseModel):
    status:str    

class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str | None = None 
    