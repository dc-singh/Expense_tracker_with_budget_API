from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.jwt_handler import verify_token
from models.category import Category
from database import get_db
from schema.category import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    new_category = Category(
        name = data.name,
        user_id = current_user["user_id"]
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user = Depends(verify_token)):
    categories = db.query(Category).filter(Category.user_id == current_user["user_id"]).all()
    return categories

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user["user_id"]).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = data.name
    
    db.commit()
    db.refresh(category)
    return category 

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user = Depends(verify_token)):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user["user_id"]).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

