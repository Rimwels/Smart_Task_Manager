from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TaskBase(BaseModel):
    title : str
    description: str

class TaskStatus(str, Enum):
    pending ="pending"
    completed = "completed"

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    status: TaskStatus
    

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    