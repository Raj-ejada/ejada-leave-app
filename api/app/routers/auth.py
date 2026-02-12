from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..security import create_access_token, verify_password, hash_password, get_db
from ..models import Employee
from ..schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.email == data.email).first()
    if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email, user.role.value)
    return {"access_token": token}

# Helper to create first admin in local dev
class RegisterIn(BaseModel):
    employee_no: str
    name: str
    email: EmailStr
    password: str

@router.post("/register-dev")
def register_dev(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(400, "Email exists")
    user = Employee(
        employee_no=data.employee_no, name=data.name,
        email=data.email, role="HR", password_hash=hash_password(data.password)
    )
    db.add(user); db.commit()
    return {"ok": True}