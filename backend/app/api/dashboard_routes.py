from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.user_model import User
from backend.app.models.institute_model import Institute

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- COE DASHBOARD ----------------
@router.get("/coe/{user_id}")
def coe_dashboard(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.role != "coe":
        raise HTTPException(403, "Not authorized")

    institute = db.query(Institute).filter(
        Institute.id == user.institute_id
    ).first()

    # 👨‍🏫 Faculty count
    faculty_count = db.query(User).filter(
        User.role == "faculty",
        User.institute_id == user.institute_id
    ).count()

    # 📄 Placeholder (we'll add real table later)
    question_papers = []

    return {
        "institute_name": institute.name,
        "faculty_count": faculty_count,
        "question_papers": question_papers
    }