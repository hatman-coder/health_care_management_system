import uuid
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from base.base import Base


class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    medical_history = Column(Text)

    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
