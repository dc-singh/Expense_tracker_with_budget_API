from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import String, Column, Integer, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    categories = relationship("Category", back_populates="owner")

    expenses = relationship("Expense", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")
    
