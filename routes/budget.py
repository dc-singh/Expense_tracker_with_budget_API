from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.budget import Budget
from models.expense import Expense
from models.category import Category
from schema.budget import BudgetCreate, BudgetResponse, BudgetStatus
from auth.jwt_handler import verify_token

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/", response_model=BudgetResponse)
def create_budget(
    data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    new_budget = Budget(
        amount=data.amount,
        month=data.month,
        category_id=data.category_id,
        user_id=current_user["user_id"]
    )
    
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    
    return new_budget

@router.get("/", response_model=list[BudgetResponse])
def get_budgets(
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    user_id = current_user["user_id"]
    
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id
    ).all()
    
    return budgets

@router.get("/status", response_model=list[BudgetStatus])
def budget_status(
    month: str,
    db: Session = Depends(get_db),
    current_user = Depends(verify_token)
):
    user_id = current_user["user_id"]
    
    # Step 1: Get all budgets for this month
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.month == month
    ).all()
    
    result = []
    year, mon = month.split("-")
    
    # Step 2: For each budget calculate actual spending
    for budget in budgets:
        
        # Sum all expenses in this category this month
        expenses = db.query(Expense).filter(
            Expense.user_id == user_id,
            Expense.category_id == budget.category_id,
            Expense.date >= f"{year}-{mon}-01",
            Expense.date <= f"{year}-{mon}-31"
        ).all()
        
        total_spent = sum(e.amount for e in expenses)
        remaining = budget.amount - total_spent
        
        # Get category name
        category = db.query(Category).filter(
            Category.id == budget.category_id
        ).first()
        
        # Build status object
        result.append(BudgetStatus(
            category=category.name,
            budget=budget.amount,
            spent=total_spent,
            remaining=remaining,
            is_exceeded=total_spent > budget.amount
        ))
    
    return result