from typing import cast
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.database.session import get_db
from app.schemas.task_schema import TaskCreate, TaskSchema, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/tasks/", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = cast(Session, Depends(get_db))):
    return TaskService.create_task(db, task)


@router.get("/tasks/", response_model=list[TaskSchema])
def list_tasks(db: Session = cast(Session, Depends(get_db)), page: int = 1, limit: int = 10):
    return TaskService.get_tasks(db, page, limit)


@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, task: TaskUpdate, db: Session = cast(Session, Depends(get_db))):
    return TaskService.update_task(db, task_id, task)


@router.delete("/tasks/{task_id}", response_model=bool)
def delete_task(task_id: int, db: Session = cast(Session, Depends(get_db))):
    return TaskService.delete_task(db, task_id)
