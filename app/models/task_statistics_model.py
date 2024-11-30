from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.schema import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime, Enum as SqlEnum, Integer
from app.database.base import Base
import enum

class TaskActionEnum(str, enum.Enum):
    created = "created"
    modified = "modified"
    deleted = "deleted"

class TaskStatistic(Base):
    __tablename__ = "task_statistics"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    action = Column(SqlEnum(TaskActionEnum), nullable=False)

    action_at = Column(DateTime(timezone=True), server_default=func.now())
