from sqlalchemy import Column, Integer, String, ForeignKey
from backend.app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)