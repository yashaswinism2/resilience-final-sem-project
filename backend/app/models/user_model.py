from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class User(Base):
    __tablename__ = "users"

    # ---------------- PRIMARY KEY ----------------
    id = Column(Integer, primary_key=True, index=True)

    # ---------------- BASIC INFO ----------------
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=True)

    # ---------------- ROLE ----------------
    role = Column(String, nullable=False)  
    # values: superadmin / coe / faculty

    # ---------------- INSTITUTE RELATION ----------------
    institute_id = Column(Integer, ForeignKey("institutes.id"), nullable=True)

    # ✅ Relationship (VERY useful later)
    institute = relationship("Institute", backref="users")

    # ---------------- STATUS ----------------
    is_active = Column(Boolean, default=True)

    # ---------------- TIMESTAMPS ----------------
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())