from infrastructure.database.sql.models.base import Base

from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    BOOLEAN,
    ForeignKey,
    Table,
    Enum,
    UniqueConstraint, JSON
)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class AssociationUserGroupUser(Base):
    __tablename__ = "association_user_group_user"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("workbench_user.id"), primary_key=True
    )
    user_group_id: Mapped[int] = mapped_column(
        ForeignKey("workbench_user_groups.id"), primary_key=True
    )

    user: Mapped["User"] = relationship(
        back_populates="asso_user")
    user_group: Mapped["UserGroup"] = relationship(
        back_populates="asso_user_group")
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserProfile(Base):
    __tablename__ = "workbench_user_profile"

    id = mapped_column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    user: Mapped[List["User"]] = relationship(
        "User",
        back_populates="user_profile"
    )


class User(Base):
    __tablename__ = "workbench_user"

    id = mapped_column(Integer, primary_key=True, autoincrement="auto")
    hash_identifier = Column(String(255), unique=True, nullable=False)
    account_id = Column(Integer, nullable=False)

    user_profile_id = Column(
        ForeignKey("workbench_user_profile.id"),
        nullable=False
    )
    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="user"
    )

    task_association: Mapped[List["AssociationTaskUser"]] = relationship(
        lazy='joined',
        back_populates="user"
    )
    tasks: Mapped[List["Task"]] = relationship(
        secondary="association_table_user_task",
        back_populates="users"
    )

    initiative_association: Mapped[List["AssociationInitiativeUser"]] = relationship(
        lazy='joined',
        back_populates="user"
    )
    initiatives: Mapped[List["Initiative"]] = relationship(
        secondary="association_table_user_initiative",
        back_populates="users"
    )

    asso_user: Mapped[List["AssociationUserGroupUser"]] = relationship(
        back_populates="user"
    )
    user_groups: Mapped[List["UserGroup"]] = relationship(
        lazy='joined',
        secondary="association_user_group_user",
        back_populates="users"
    )


class UserGroup(Base):
    __tablename__ = "workbench_user_groups"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    roles: Mapped[List["Role"]] = relationship(back_populates="group")
    asso_user_group: Mapped[List["AssociationUserGroupUser"]] = relationship(
        back_populates="user_group"
    )
    users: Mapped[List["User"]] = relationship(
        lazy='joined',
        secondary="association_user_group_user",
        back_populates="user_groups"
    )


class Role(Base):

    __tablename__ = "workbench_user_group_roles"
    __table_args__ = (
        UniqueConstraint(
            'user_group_id',
            'name',
            name='unique_name_role_user_group'
        ),
    )
    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_group_id = Column(Integer, ForeignKey("workbench_user_groups.id"))
    name = Column(String(100))
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(
        lazy='joined',
        back_populates="roles"
    )
