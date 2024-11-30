from typing import Optional
from typing_extensions import List
from sqlalchemy.orm.session import Session

from app.models.task_model import Task, TaskStatusEnum
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

    @staticmethod
    def bulk_delete_tasks(db: Session, task_ids: List[int]) -> List[int]:
        """
        Perform bulk soft delete of tasks

        Args:
            db (Session): Database session
            task_ids (List[int]): List of task IDs to delete

        Returns:
            List[int]: List of successfully deleted task IDs
        """

        # Find existing, non-deleted tasks
        existing_tasks = db.query(Task).filter(
            Task.id.in_(task_ids),
            Task.is_deleted == False
        ).all()

        # Track successfully deleted task IDs
        deleted_task_ids: list[int] = []

        # Soft delete tasks and log statistics for each
        for task in existing_tasks:
            task.is_deleted = True

            # Log deletion action
            StatisticsService.log_action(db, task.id, TaskActionEnum.deleted)

            deleted_task_ids.append(task.id)

        # Commit changes if we have any deletions
        if deleted_task_ids:
            db.commit()

        return deleted_task_ids

    @staticmethod
    def bulk_complete_tasks(db: Session, task_ids: List[int]) -> List[int]:
        """
        Perform bulk marking of tasks as complete

        Args:
            db (Session): Database session
            task_ids (List[int]): List of task IDs to mark complete

        Returns:
            List[int]: List of successfully completed task IDs
        """
        # Find existing, non-deleted tasks that are not already completed
        existing_tasks = db.query(Task).filter(
            Task.id.in_(task_ids),
            Task.is_deleted == False,
            Task.status != TaskStatusEnum.completed
        ).all()

        # Track successfully completed task IDs
        completed_task_ids: list[int] = []

        # Mark tasks as complete and log statistics for each
        for task in existing_tasks:
            task.status = TaskStatusEnum.completed

            # Log modification action
            StatisticsService.log_action(db, task.id, TaskActionEnum.modified)

            completed_task_ids.append(task.id)

        # Commit changes if we have any completions
        if completed_task_ids:
            db.commit()

        return completed_task_ids
