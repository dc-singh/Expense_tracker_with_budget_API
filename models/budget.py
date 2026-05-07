from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer,primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    month = Column(String(7), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    owner = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")