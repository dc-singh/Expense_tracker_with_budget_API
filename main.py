from fastapi import FastAPI, Depends
from database import get_db
from sqlalchemy.orm import Session

app =FastAPI(title="Expense Tracker API", description="API for Expense Tracking", version="1.0.0")

@app.get("/")
def read_root():
    return {"MSG": "Hello World"}

@app.get("/DBConnection")
def getdb(db: Session = Depends(get_db)):
    return {"MSG": "Connection Successfull"}