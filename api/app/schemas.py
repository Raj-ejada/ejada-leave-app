from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List
from .models import Role, Status, Decision

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    employee_no: str
    name: str
    email: EmailStr
    role: Role
    class Config: orm_mode = True

class LeaveRequestCreate(BaseModel):
    leave_type_id: int
    reason: Optional[str] = None
    start_date: date
    end_date: date
    is_half_day: bool = False

class LeaveRequestOut(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    status: Status
    reason: Optional[str]
    start_date: date
    end_date: date
    days: float
    is_half_day: bool
    created_at: datetime
    updated_at: datetime
    class Config: orm_mode = True

class ApprovalIn(BaseModel):
    decision: Decision
    comments: Optional[str] = None

class LeaveBalanceOut(BaseModel):
    leave_type_id: int
    year: int
    opening: float
    credited: float
    availed: float
    adjusted: float
    closing: float
    class Config: orm_mode = True
