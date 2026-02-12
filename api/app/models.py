from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, Enum, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class Role(str, enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"
    HR = "HR"

class Decision(str, enum.Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Status(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    employee_no = Column(String(20), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    designation = Column(String(120))
    department_id = Column(Integer, ForeignKey("departments.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    role = Column(Enum(Role), default=Role.EMPLOYEE, nullable=False)
    is_active = Column(Boolean, default=True)
    password_hash = Column(String(255), nullable=True)  # local auth only
    created_at = Column(DateTime, default=datetime.utcnow)

    department = relationship("Department")
    manager = relationship("Employee", remote_side=[id])

class LeaveType(Base):
    __tablename__ = "leave_types"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    default_annual_quota = Column(Float, default=0)
    carry_forward_limit = Column(Float, default=0)
    requires_document = Column(Boolean, default=False)

class LeaveBalance(Base):
    __tablename__ = "leave_balances"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    year = Column(Integer, nullable=False)
    opening = Column(Float, default=0)
    credited = Column(Float, default=0)
    availed = Column(Float, default=0)
    adjusted = Column(Float, default=0)
    closing = Column(Float, default=0)

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    status = Column(Enum(Status), default=Status.DRAFT, nullable=False)
    reason = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Float, default=0)
    is_half_day = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("leave_requests.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    role = Column(Enum(Role), nullable=False)
    decision = Column(Enum(Decision), nullable=False)
    comments = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=datetime.utcnow)

class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    name = Column(String(120), nullable=False)
    region = Column(String(50), nullable=True)

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("leave_requests.id"), nullable=False)
    s3_key = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    content_type = Column(String(80), nullable=False)
    size = Column(Integer, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
