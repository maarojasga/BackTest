from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContactCreate(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: Optional[str] = None
    website: Optional[str] = None

class APILogCreate(BaseModel):
    endpoint: str
    request_data: str
    result: str
