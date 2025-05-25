from sqlalchemy.orm import Session
import models
from sqlalchemy.exc import SQLAlchemyError
from schema import CreateComplaints
from helper import generate_complaint_id


class ComplaintsService:
    @classmethod
    def get_complaints(cls, db: Session, complaint_id: str):
        try:
            return db.query(models.Complaint).filter(models.Complaint.complaint_id == complaint_id).first()
        except SQLAlchemyError as e:
            raise  
        
    @classmethod
    def create_complaint(cls, db: Session, data: CreateComplaints):
        try:
            complaint_id = generate_complaint_id()
            new_complaint = models.Complaint(
                complaint_id=complaint_id,
                name=data.name,
                phone_number=data.phone_number,
                email=data.email,
                complaint_details=data.complaint_details
            )
            db.add(new_complaint)
            db.commit()
            db.refresh(new_complaint)
            return complaint_id

        except SQLAlchemyError as e:
            db.rollback()  
            raise 