from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..security import get_db, require_role
from ..models import LeaveRequest, Status, Approval, Role, LeaveBalance
from ..schemas import ApprovalIn

router = APIRouter(prefix="/approvals", tags=["approvals"])

@router.get("/pending")
def pending(db: Session = Depends(get_db), user=Depends(require_role(Role.MANAGER, Role.HR))):
    # Manager sees direct reports; HR sees all
    q = db.query(LeaveRequest).filter(LeaveRequest.status == Status.SUBMITTED)
    if user.role == Role.MANAGER:
        q = q.filter(LeaveRequest.employee_id.in_([e.id for e in [*db.query(type(user)).filter(type(user).manager_id == user.id)]]))
    return [ {"id":lr.id, "employee_id":lr.employee_id, "start_date":str(lr.start_date), "end_date":str(lr.end_date), "days":lr.days} for lr in q.all() ]

@router.patch("/{req_id}/decide")
def decide(req_id: int, data: ApprovalIn, db: Session = Depends(get_db), user=Depends(require_role(Role.MANAGER, Role.HR))):
    lr = db.query(LeaveRequest).get(req_id)
    if not lr or lr.status != Status.SUBMITTED:
        raise HTTPException(404, "Invalid request")
    # create approval record
    app = Approval(request_id=lr.id, approver_id=user.id, role=user.role, decision=data.decision, comments=data.comments, decided_at=datetime.utcnow())
    db.add(app)

    if data.decision.name == "APPROVED":
        # HR final approval sets APPROVED; for MVP manager directly approves.
        lr.status = Status.APPROVED
        # adjust balance
        # Skip for UNPAID
        # ... fetch balance & update
        # (MVP): decrement availed & closing
        # (Safe check): only if not UNPAID
        # This is simplified; production should handle year crossing, etc.
        # Get leave type
        lt_id = lr.leave_type_id
        year = lr.start_date.year
        bal = db.query(LeaveBalance).filter_by(employee_id=lr.employee_id, leave_type_id=lt_id, year=year).first()
        if bal:
            bal.availed += lr.days
            bal.closing = bal.opening + bal.credited + bal.adjusted - bal.availed
    else:
        lr.status = Status.REJECTED

    lr.updated_at = datetime.utcnow()
    db.commit()
    return {"ok": True, "status": lr.status.name}