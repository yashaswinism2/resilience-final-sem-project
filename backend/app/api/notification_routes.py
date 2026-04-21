from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.notification_model import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- GET NOTIFICATIONS ----------------
@router.get("/{faculty_id}")
def get_notifications(faculty_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(
        Notification.faculty_id == faculty_id
    ).all()

    return notifications