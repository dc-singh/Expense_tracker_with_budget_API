from sqlalchemy import Integer, Column, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(250), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="owner")
    expenses = relationship("Expenses", back_populates="owner")
    budgets = relationship("Budgets", back_populates="owner")