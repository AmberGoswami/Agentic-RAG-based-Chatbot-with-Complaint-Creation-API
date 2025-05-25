from pydantic import BaseModel, EmailStr
from datetime import datetime

class ShowComplaints(BaseModel):
    complaint_id:str
    name:str
    phone_number:str
    email:str
    complaint_details:str
    created_at:datetime
    class Config:
        from_attributes = True
    
class CreateComplaints(BaseModel):
    name: str
    phone_number: str
    email: EmailStr
    complaint_details: str
    class Config:
        from_attributes = True
    
class CreateComplaintstResponse(BaseModel):
    complaint_id: str
    message: str
    class Config:
        from_attributes = True