import logging
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from api.complaints.complaints_service import ComplaintsService
from fastapi import APIRouter,Depends,HTTPException, Path, status
from schema import ShowComplaints, CreateComplaints, CreateComplaintstResponse


class ComplaintsController: 
        
    router = APIRouter(
        prefix="/complaints",
        tags=["complaints"],
    )
    
    @router.get('/{complaint_id}', response_model=ShowComplaints)
    def get_complaint_by_id(complaint_id: str = Path(...), db: Session = Depends(get_db)):
        try:
            complaint = ComplaintsService.get_complaints(db, complaint_id)
            if not complaint:
                raise HTTPException(status_code=404, detail="Complaint not found")
            return complaint
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Database error occurred")
        
    @router.post('/', response_model=CreateComplaintstResponse, status_code=status.HTTP_201_CREATED)
    def create_complaint(complaint_data: CreateComplaints, db: Session = Depends(get_db)):
        try:
            complaint_id = ComplaintsService.create_complaint(db, complaint_data)
            return {"complaint_id": complaint_id, "message": "Complaint created successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error occurred")