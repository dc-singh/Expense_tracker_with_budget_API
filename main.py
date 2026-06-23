from fastapi import FastAPI
from database import Base, engine
from models.user import User
from models.category import Category
from models.expense import Expense
from models.budget import Budget
from routes import auth, categories, expenses


app = FastAPI(title="Expense Tracker & Budgeting API", version="1.0.0")

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
# app.include_router(Budget.router)



@app.get("/")
def root():
    return {"msg":"Done"}
