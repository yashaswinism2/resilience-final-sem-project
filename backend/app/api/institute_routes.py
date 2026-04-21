from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.institute_model import Institute

router = APIRouter(prefix="/institutes", tags=["Institutes"])


# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- CREATE INSTITUTE ----------------
@router.post("/")
def create_institute(name: str, db: Session = Depends(get_db)):

    existing = db.query(Institute).filter(Institute.name == name).first()
    if existing:
        raise HTTPException(400, "Institute already exists")

    institute = Institute(name=name)

    db.add(institute)
    db.commit()
    db.refresh(institute)

    return {
        "message": "Institute created successfully",
        "id": institute.id,
        "name": institute.name
    }


# ---------------- GET ALL INSTITUTES ----------------
@router.get("/")
def get_institutes(db: Session = Depends(get_db)):

    institutes = db.query(Institute).all()

    return institutes

@router.get("/{institute_id}")
def get_institute(institute_id: int, db: Session = Depends(get_db)):

    institute = db.query(Institute).filter(
        Institute.id == institute_id
    ).first()

    if not institute:
        raise HTTPException(404, "Institute not found")

    return institute