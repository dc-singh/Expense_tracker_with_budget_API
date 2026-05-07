from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class config:
    from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    name: str

