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
@router.put("/{paper_id}/status")
def update_status(paper_id: int, data: dict, db: Session = Depends(get_db)):

    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id
    ).first()

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # ✅ update status
    paper.status = data.get("status")

    db.commit()

    return {"message": f"Paper {paper.status} successfully"}