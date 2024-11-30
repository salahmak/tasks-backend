from sqlalchemy import Column
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Enum as SqlEnum, String, Text
from sqlalchemy.types import Integer
from app.database.base import Base
from enum import Enum

class TaskStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    status: Mapped[TaskStatusEnum] = mapped_column(SqlEnum(TaskStatusEnum), default=TaskStatusEnum.pending)


    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
