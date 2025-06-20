from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from datetime import datetime
from .permission import role_permissions # Import the association table

# Association table for User and Role
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

# The role_permissions table is now defined in app/models/permission.py
# and imported on line 6.

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

# The Permission model is now defined in app/models/permission.py
# class Permission(Base):
#    __tablename__ = "permissions"
#
#    id = Column(Integer, primary_key=True, index=True)
#    name = Column(String, unique=True, index=True)
#    description = Column(String)
#    resource = Column(String)
#    action = Column(String)
#    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#    roles = relationship("Role", secondary=role_permissions, back_populates="permissions") 