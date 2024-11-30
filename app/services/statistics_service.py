from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import and_

from app.models.task_model import Task, TaskStatusEnum
from app.models.task_statistics_model import TaskActionEnum, TaskStatistic
from app.schemas.task_statistic_schema import TaskStatisticsOverviewSchema


class StatisticsService:
    @staticmethod
    def log_action(db: Session, task_id: int, action_type: TaskActionEnum):
        """
        Log a task action in the statistics
        """
        task_stat = TaskStatistic(task_id=task_id, action=action_type)
        db.add(task_stat)
        db.commit()
        return task_stat

    @staticmethod
    def get_task_statistics(db: Session) -> TaskStatisticsOverviewSchema:
        """
        Get comprehensive task statistics
        """
        # Total tasks (excluding soft-deleted)
        total_tasks = db.query(Task).filter(Task.is_deleted == False).count()

        # Modified tasks
        modified_tasks = db.query(TaskStatistic)\
            .filter(TaskStatistic.action == TaskActionEnum.modified)\
            .count()

        # Deleted tasks
        deleted_tasks = db.query(TaskStatistic)\
            .filter(TaskStatistic.action == TaskActionEnum.deleted)\
            .count()

        # Completed tasks
        completed_tasks = db.query(Task)\
            .filter(and_(
                Task.status == TaskStatusEnum.completed,
                Task.is_deleted == False
            ))\
            .count()

        return TaskStatisticsOverviewSchema(
            total_tasks=total_tasks,
            modified_tasks=modified_tasks,
            deleted_tasks=deleted_tasks,
            completed_tasks=completed_tasks
        )

    @staticmethod
    def get_paginated_task_actions(
        db: Session,
        limit: int = 10,
        page: int = 1
    ):
        """
        Get paginated task actions with total count
        """
        # Calculate offset
        offset = (page - 1) * limit

        # Get total count of actions
        total_actions = db.query(func.count(TaskStatistic.id)).scalar()

        # Get paginated actions
        task_actions = db.query(TaskStatistic)\
            .order_by(TaskStatistic.action_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()

        return {
            'actions': task_actions,
            'total_actions': total_actions
        }
