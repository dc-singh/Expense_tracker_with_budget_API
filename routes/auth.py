from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import password
from database import get_db
from models.user import User
from schema.user import UserCreate, UserLogin, UserResponse, TokenResponse
from auth.password import hash_password, verify_password
from auth.jwt_handler import create_access_token, verify_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail = "Email already registered")
    
    hashed = hash_password(data.password)

    new_user = User(
        name=data.name,
        email=data.email,
        password = hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({'user_id': user.id,
                                 'email': user.email})
    
    return {"access_token": token}

@router.get("/me", response_model=UserResponse)
def get_current_user(db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
    user_id = current_user["user_id"]
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

