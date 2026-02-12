from datetime import timedelta
from sqlalchemy.orm import Session
from ..models import Holiday
import datetime as dt

def business_days(db: Session, start, end, include_weekends=False) -> int:
    if start > end:
        return 0
    delta = end - start
    days = 0
    holidays = {h.date for h in db.query(Holiday).all()}
    for i in range(delta.days + 1):
        d = start + timedelta(days=i)
        if not include_weekends and d.weekday() >= 5:
            continue
        if d in holidays:
            continue
        days += 1
    return days