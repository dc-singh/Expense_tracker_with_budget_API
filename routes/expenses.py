from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.expense import Expense
from schema.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from auth.jwt_handler import verify_token

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    new_expense = Expense(
        title = data.title,
        amount = data.amount,
        note = data.note,
        date = data.date,
        category_id = data.category_id,
        user_id = current_user["user_id"]
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=list[ExpenseResponse])
def all_expenses(
    category_id: Optional[int] = None,
    month: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    user_id = current_user["user_id"]
    
    query = db.query(Expense).filter(Expense.user_id == user_id)
    
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    
    if month:
        year, mon = month.split("-")
        query = query.filter(
            Expense.date >= f"{year}-{mon}-01",
            Expense.date <= f"{year}-{mon}-31"
        )
    
    if min_amount:
        query = query.filter(Expense.amount >= min_amount)
    
    if max_amount:
        query = query.filter(Expense.amount <= max_amount)
    
    return query.order_by(Expense.date.desc()).all()


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_single_expense(expense_id: int, db: Session = Depends(get_db), current_user = Depends(verify_token)):

    user_id = current_user["user_id"]

    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    user_id = current_user["user_id"]

    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}",)
def expense_delete(expense_id: int, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    user_id = current_user["user_id"]

    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    
    return {"message": "Expense deleted successfully"}
    