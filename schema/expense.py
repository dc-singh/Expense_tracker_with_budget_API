from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    date: date
    note: Optional[str] = None
    category_id: int

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None
    note: Optional[str] = None
    category_id: Optional[int] = None
    
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category_id: int
    date: date
    note: Optional[str] = None
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True