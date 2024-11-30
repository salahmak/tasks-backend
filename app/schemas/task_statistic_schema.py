import datetime
from pydantic import Field
from pydantic.main import BaseModel
from app.models.task_statistics_model import TaskActionEnum


class TaskStatisticBase(BaseModel):
    action: TaskActionEnum = Field(..., description="Task action")


class TaskStatisticSchema(TaskStatisticBase):
    id: int = 0
    task_id: int = 0

    action_at: datetime.datetime

    class Config:
        orm_mode = True
