from enum import Enum
from typing_extensions import List
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.models.task_model import TaskStatusEnum

class TaskSortingModeEnum(str, Enum):
    asc = "asc"
    desc = "desc"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Optional task description")
    status: TaskStatusEnum = Field(TaskStatusEnum.pending, description="Task status")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_deleted: Optional[bool] = Field(False, description="Mark task as deleted")
    status: Optional[TaskStatusEnum] = Field(None, description="Update task status")

class TasksBulkAction(BaseModel):
    task_ids: List[int] = Field(..., min_length=1, description="List of task IDs to be acted upon")

class TaskSchema(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False

    class Config:
        orm_mode = True
