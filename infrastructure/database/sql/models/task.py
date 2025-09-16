from typing import List

from infrastructure.database.sql.models.base import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String, ARRAY, ForeignKey
)

from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column


class AssociationTaskUser(Base):
    __tablename__ = "association_table_user_task"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("workbench_user.id"),
        primary_key=True
    )
    task: Mapped["Task"] = relationship(back_populates="user_association")
    user: Mapped["User"] = relationship(back_populates="task_association")
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement="auto")

    title = Column(String(255), nullable=False)
    description = Column(TEXT, nullable=True)
    priority = Column(Integer, nullable=True)
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)

    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    initiative_id = Column(ForeignKey('initiative.id'), nullable=False)
    initiative: Mapped["Initiative"] = relationship(
        lazy='joined',
        back_populates="tasks"
    )

    users: Mapped[List["User"]] = relationship(
        lazy='joined',
        secondary='association_table_user_task',
        back_populates='tasks'
    )
    user_association: Mapped[List["AssociationTaskUser"]] = relationship(
        lazy='joined',
        back_populates='task'
    )