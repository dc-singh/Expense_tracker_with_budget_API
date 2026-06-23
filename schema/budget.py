from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class BudgetCreate(BaseModel):
    amount: float
    month: str
    category_id: int

class BudgetResponse(BaseModel):
    id: int
    amount: float
    month: str
    category_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BudgetStatus(BaseModel):
    category: str
    budget: float
    spent: float
    remaining: float
    is_exceeded: bool
