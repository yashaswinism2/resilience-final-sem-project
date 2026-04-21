from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import SessionLocal
from backend.app.models.user_model import User
from backend.app.models.institute_model import Institute  # ✅ NEW
from backend.app.schemas.user_schema import UserCreate, UserLogin
from backend.app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Allowed roles
ALLOWED_ROLES = ["superadmin", "coe", "faculty"]


# ---------------- SIGNUP ----------------
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    print("🔥 Signup request received:", user)

    try:
        # ✅ Role validation
        if user.role not in ALLOWED_ROLES:
            raise HTTPException(400, "Invalid role")

        # ✅ Password length check
        if len(user.password) > 72:
            raise HTTPException(400, "Password too long (max 72 characters)")

        # ✅ Check if user exists
        existing = db.query(User).filter(User.username == user.username).first()
        if existing:
            raise HTTPException(400, "Username already exists")

        # ---------------- ROLE RULES ----------------

        # ✅ Superadmin → no institute
        if user.role == "superadmin":
            institute_id = None

        # ✅ COE / Faculty → must have valid institute
        else:
            if not user.institute_id:
                raise HTTPException(400, "Institute required for COE/Faculty")

            institute = db.query(Institute).filter(
                Institute.id == user.institute_id
            ).first()

            if not institute:
                raise HTTPException(400, "Invalid institute")

            institute_id = user.institute_id

        # ---------------- CREATE USER ----------------
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            password=hash_password(user.password),
            role=user.role,
            institute_id=institute_id  # ✅ IMPORTANT
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(
            "✅ User created:",
            new_user.username,
            "| Role:",
            new_user.role,
            "| Institute:",
            new_user.institute_id
        )

        return {"message": "User created successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(500, "Internal server error")


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    print("🔐 Login attempt:", user.username, "| Role:", user.role)

    try:
        # ✅ Check username + role
        db_user = db.query(User).filter(
            User.username == user.username,
            User.role == user.role
        ).first()

        if not db_user:
            raise HTTPException(401, "Invalid username, role, or password")

        # ✅ Check password
        if not verify_password(user.password, db_user.password):
            raise HTTPException(401, "Invalid username, role, or password")

        print("✅ Login successful")

        return {
            "message": "Login successful",
            "username": db_user.username,
            "role": db_user.role,
            "user_id": db_user.id,
            "institute_id": db_user.institute_id
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(500, "Internal server error")
    
from backend.app.models.institute_model import Institute

@router.post("/superadmin-signup")
def superadmin_signup(data: dict, db: Session = Depends(get_db)):

    institute = Institute(name=data["institute_name"])
    db.add(institute)
    db.commit()
    db.refresh(institute)

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        username=data["username"],
        password=hash_password(data["password"]),
        role="superadmin",
        institute_id=institute.id
    )

    db.add(user)
    db.commit()

    return {"message": "Superadmin + Institute created"}