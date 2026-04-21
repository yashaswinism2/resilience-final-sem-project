from pydantic import BaseModel, validator
from typing import Optional

# ✅ Allowed roles
ALLOWED_ROLES = ["superadmin", "coe", "faculty"]


# ---------------- CREATE USER ----------------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: str
    institute_id: Optional[int] = None  # ✅ NEW

    # ✅ Validate role
    @validator("role")
    def validate_role(cls, value):
        if value not in ALLOWED_ROLES:
            raise ValueError("Invalid role")
        return value

    # ✅ Validate institute rules
    @validator("institute_id", always=True)
    def validate_institute(cls, value, values):
        role = values.get("role")

        # Superadmin should NOT have institute
        if role == "superadmin" and value is not None:
            raise ValueError("Superadmin should not have institute")

        # COE and Faculty MUST have institute
        if role in ["coe", "faculty"] and value is None:
            raise ValueError("Institute is required for COE and Faculty")

        return value


# ---------------- LOGIN USER ----------------
class UserLogin(BaseModel):
    username: str
    password: str
    role: str

    # ✅ Validate role
    @validator("role")
    def validate_role(cls, value):
        if value not in ALLOWED_ROLES:
            raise ValueError("Invalid role")
        return value