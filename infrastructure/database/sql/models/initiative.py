from typing import List
from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    String,
    Boolean
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TEXT

from infrastructure.database.sql.models.base import Base


class AssociationInitiativeUser(Base):
    __tablename__ = "association_table_user_initiative"

    initiative_id: Mapped[int] = mapped_column(
        ForeignKey("initiative.id"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("workbench_user.id"),
        primary_key=True
    )
    notification = Column(Boolean, default=False)
    initiative: Mapped["Initiative"] = relationship(
        back_populates="user_association"
    )
    user: Mapped["User"] = relationship(
        back_populates="task_association"
    )
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class InitiativeLocation(Base):
    __tablename__ = "initiative_location"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    city =  Column(String(100), nullable=False)
    street =  Column(String(255), nullable=False)
    number = Column(String(20), nullable=False)

    initiatives: Mapped[List["Initiative"]] = relationship(
        back_populates='location'
    )

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


class InitiativeAttendee(Base):
    __tablename__ = "initiative_attendee"

    id = Column(Integer, primary_key=True, autoincrement="auto")

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    notification = Column(Boolean, default=False)

    initiatives: Mapped[List["Initiative"]] = relationship(
        back_populates='type'
    )


class Initiative(Base):
    """
        Wydarzenia, pomoc społeczna, Edukacja, Ekologia, Wsparcie
    """
    __tablename__ = "initiative"

    id = Column(Integer, primary_key=True, autoincrement="auto")

    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    custom_notes = Column(TEXT, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    attendee_id = Column(ForeignKey('InitiativeAttendee.id'), nullable=True)
    attendee: Mapped["InitiativeAttendee"] = relationship(
        back_populates='initiatives'
    )

    location_id = Column(ForeignKey('InitiativeLocation.id'), nullable=True)
    location: Mapped["InitiativeLocation"] = relationship(
        back_populates='initiatives'
    )

    type_id = Column(Integer, ForeignKey(InitiativeType.id), nullable=False)
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