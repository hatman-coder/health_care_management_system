import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from base.base import Base
from external.enum import AppointmentStatus, PaymentStatus


class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.doctor_id"))
    date_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.FAILED)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
