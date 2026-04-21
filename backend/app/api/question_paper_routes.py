from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json

from backend.app.db.database import SessionLocal
from backend.app.models.question_paper_model import QuestionPaper

router = APIRouter(prefix="/papers", tags=["Question Papers"])


# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- GET PAPERS BY INSTITUTE (COE) ----------------
@router.get("/institute/{institute_id}")
def get_papers(institute_id: int, db: Session = Depends(get_db)):

    papers = db.query(QuestionPaper).filter(
        QuestionPaper.institute_id == institute_id
    ).all()

    # ✅ Convert SQLAlchemy objects to dict
    result = []
    for paper in papers:
        result.append({
            "id": paper.id,
            "faculty_id": paper.faculty_id,
            "institute_id": paper.institute_id,
            "status": paper.status,
            "content": paper.content,  # keep as JSON string
        })

    return result


# ---------------- SUBMIT PAPER ----------------
@router.post("/submit")
def submit_paper(data: dict, db: Session = Depends(get_db)):

    import json

    try:
        paper = QuestionPaper(
            content=json.dumps(data["questions"]),
            faculty_id=data["faculty_id"],
            institute_id=data["institute_id"],
            status="pending"
        )

        db.add(paper)
        db.commit()
        db.refresh(paper)

        return {"message": "Paper sent to COE"}

    except Exception as e:
        db.rollback()  # ✅ prevents DB lock
        raise e

from fastapi import HTTPException


# ---------------- UPDATE STATUS (COE) ----------------
from fastapi import HTTPException
from backend.app.models.notification_model import Notification

@router.put("/{paper_id}/status")
def update_status(paper_id: int, data: dict, db: Session = Depends(get_db)):

    # 🔍 Find paper
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id
    ).first()

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # ✅ Validate status
    status = data.get("status")
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        # ✅ Update status
        paper.status = status

        # 🔔 Create notification
        message = f"Your question paper (ID: {paper.id}) is {status}"

        notification = Notification(
            faculty_id=paper.faculty_id,
            message=message
        )

        db.add(notification)

        # ✅ Save changes
        db.commit()
        db.refresh(paper)

        return {"message": f"Paper {status} successfully"}

    except Exception as e:
        db.rollback()
        raise e