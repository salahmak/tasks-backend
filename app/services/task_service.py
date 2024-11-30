from typing import Optional
from sqlalchemy.orm.session import Session

from app.models.task_model import Task
from app.models.task_statistics_model import TaskActionEnum, TaskStatistic
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.services.statistics_service import StatisticsService


class TaskService:

    @staticmethod
    def get_total_task_count(db: Session) -> int:
        """
        Get the total count of non-deleted tasks
        """
        return db.query(Task).filter(Task.is_deleted == False).count()

    @staticmethod
    def get_tasks(db: Session, page: int = 1, limit: int = 10):
        return db.query(Task).filter(Task.is_deleted == False).offset((page - 1) * limit).limit(limit).all()


    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:

        # create the new task and add it to the database
        db_task = Task(title=task.title, description=task.description)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # update the statistics
        StatisticsService.log_action(db, db_task.id, TaskActionEnum.created)

        return db_task


    @staticmethod
    def update_task(db: Session, task_id: int, updated_task: TaskUpdate) -> Optional[Task]:
        # find existing Task
        db_task = db.query(Task).filter(Task.id == task_id).first()

        # if the task does not exist or is softly deleted, return None
        if not db_task or db_task.is_deleted:
            return None

        # update the task
        for key, value in updated_task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)

        # update the statistics
        StatisticsService.log_action(db, db_task.id, TaskActionEnum.modified)

        db.commit()
        db.refresh(db_task)

        return db_task


    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        # Soft delete the task
        db_task = db.query(Task).filter(Task.id == task_id).first()

        if not db_task or db_task.is_deleted:
            return False

        db_task.is_deleted = True

        # Update task statistics
        StatisticsService.log_action(db, db_task.id, TaskActionEnum.deleted)

        db.commit()

        return True
