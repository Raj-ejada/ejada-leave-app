from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from ..security import get_current_user, get_db
from ..models import LeaveRequest, LeaveType, LeaveBalance, Status
from ..schemas import LeaveRequestCreate, LeaveRequestOut
from ..utils.dates import business_days
from ..utils.email import send_email

router = APIRouter(prefix="/leave-requests", tags=["leave"])

@router.post("", response_model=LeaveRequestOut)
def create_leave(req: LeaveRequestCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lt = db.query(LeaveType).get(req.leave_type_id)
    if not lt:
        raise HTTPException(404, "Leave type not found")
    if req.start_date > req.end_date:
        raise HTTPException(400, "Start > End")
    days = business_days(db, req.start_date, req.end_date)
    if req.is_half_day: days = 0.5

    # Balance check (ignore for UNPAID)
    if lt.code != "UNPAID":
        year = req.start_date.year
        bal = db.query(LeaveBalance).filter_by(employee_id=user.id, leave_type_id=lt.id, year=year).first()
        if not bal or (bal.closing - days) < -0.0001:
            raise HTTPException(400, "Insufficient balance")

    lr = LeaveRequest(
        employee_id=user.id, leave_type_id=lt.id, status=Status.DRAFT,
        reason=req.reason, start_date=req.start_date, end_date=req.end_date, days=days,
        is_half_day=req.is_half_day, updated_at=datetime.utcnow()
    )
    db.add(lr); db.commit(); db.refresh(lr)
    return lr

@router.get("", response_model=list[LeaveRequestOut])
def list_mine(status: Status | None = Query(None), db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(LeaveRequest).filter(LeaveRequest.employee_id == user.id)
    if status: q = q.filter(LeaveRequest.status == status)
    return q.order_by(LeaveRequest.created_at.desc()).all()

@router.patch("/{req_id}/submit")
def submit(req_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    lr = db.query(LeaveRequest).get(req_id)
    if not lr or lr.employee_id != user.id:
        raise HTTPException(404, "Not found")
    if lr.status != Status.DRAFT:
        raise HTTPException(400, "Only draft can be submitted")
    lr.status = Status.SUBMITTED
    lr.updated_at = datetime.utcnow()
    db.commit()

    # Email manager (if any)
    if user.manager and user.manager.email:
        send_email(user.manager.email, "New Leave Request Submitted", f"{user.name} submitted leave #{lr.id}")
    return {"ok": True}
