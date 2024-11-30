from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func

from app.models.task_statistics_model import TaskActionEnum, TaskStatistic


class StatisticsService:
    @staticmethod
    def log_action(db: Session, task_id: int, action_type: TaskActionEnum):

        task_stat = TaskStatistic(task_id=task_id, action=action_type)

        db.add(task_stat)

        db.commit()

        return task_stat

    @staticmethod
    def get_task_statistics(db: Session):
        """
        Get the statistics of the tasks
        """

        task_stats_counts = db.query(TaskStatistic.action, func.count(TaskStatistic.id).label("count")).group_by(TaskStatistic.action).all()

        total_actions = db.query(func.count(TaskStatistic.id)).scalar()


        # Todo: use a data transfer object instead of a dictionary
        return {
            "total_actions": total_actions,
            "statistics": {action: count for action, count in task_stats_counts}
        }

    @staticmethod
    def get_paginated_last_actions(db: Session, limit: int = 10, page: int = 1):
        """
        Get the last actions performed on the tasks
        """

        task_stats = db.query(TaskStatistic).order_by(TaskStatistic.created_at.desc()).limit(limit).offset((page - 1) * limit).all()

        return task_stats
