import datetime
from pydantic import Field
from pydantic.main import BaseModel
from app.models.task_statistics_model import TaskActionEnum


class TaskStatisticSchema(BaseModel):
    id: int
    task_id: int
    action: TaskActionEnum
    action_at: datetime.datetime

    class Config:
        from_attributes = True

class TaskStatisticsOverviewSchema(BaseModel):
    total_tasks: int = Field(..., description="Total number of tasks")
    modified_tasks: int = Field(..., description="Number of modified tasks")
    deleted_tasks: int = Field(..., description="Number of deleted tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
