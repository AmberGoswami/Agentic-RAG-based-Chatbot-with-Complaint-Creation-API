from sqlalchemy import (
    Column, Integer, String, Text, DateTime, func
)
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(
        String(36), unique=True, nullable=False,
    )
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    complaint_details = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False,
        server_default=func.now()
    )

    def __repr__(self):
        return (
            f"<Complaint(complaint_id={self.complaint_id}, "
            f"name={self.name}, created_at={self.created_at})>"
        )
