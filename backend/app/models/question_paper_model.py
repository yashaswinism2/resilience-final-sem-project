from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from backend.app.db.database import Base


class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=True)

    content = Column(Text)  # store generated questions JSON/string

    faculty_id = Column(Integer, ForeignKey("users.id"))
    institute_id = Column(Integer, ForeignKey("institutes.id"))

    status = Column(String, default="pending")  # pending / approved / rejected

    created_at = Column(DateTime, server_default=func.now())