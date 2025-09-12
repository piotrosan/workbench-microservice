from typing import List
from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TEXT

from infrastructure.database.sql.models.base import Base


class AssociationInitiativeUser(Base):
    __tablename__ = "association_table_user_initiative"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("Task.id"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id"),
        primary_key=True
    )
    initiative: Mapped["Initiative"] = relationship(
        back_populates="user_association")
    user: Mapped["User"] = relationship(back_populates="task_association")
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class InitiativeType(Base):
    __tablename__ = "initiative_type"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    initiatives: Mapped[List["Initiative"]] = relationship(
        back_populates='type'
    )

class Initiative(Base):
    """
        Wydarzenia, pomoc społeczna, Edukacja, Ekologia, Wsparcie
    """
    __tablename__ = "initiative"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    type_id = Column(Integer, ForeignKey(InitiativeType.id), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    custom_notes = Column(TEXT, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    type: Mapped["InitiativeType"] = relationship(
        back_populates='initiatives'
    )

    tasks: Mapped[List["Task"]] = relationship(
        lazy='joined',
        back_populates="initiative"
    )

    users: Mapped[List["User"]] = relationship(
        lazy='joined',
        secondary='association_table_user_initiative',
        back_populates='initiatives'
    )
    user_association: Mapped[List["AssociationInitiativeUser"]] = relationship(
        lazy='joined',
        back_populates='task'
    )