from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from base.base import Base


class Specialty(Base):
    __tablename__ = "specialties"

    specialty_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)

    # Reverse relationship from Specialty to Doctor
    doctors = relationship(
        "Doctor", secondary="doctor_specialties", back_populates="specialties"
    )


class DoctorSpecialty(Base):
    __tablename__ = "doctor_specialties"

    doctor_id = Column(
        UUID(as_uuid=True), ForeignKey("doctors.doctor_id"), primary_key=True
    )
    specialty_id = Column(
        UUID(as_uuid=True), ForeignKey("specialties.specialty_id"), primary_key=True
    )


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    profile_details = Column(String)

    # Relationship with User
    user = relationship("User", back_populates="doctor")

    # Many-to-many relationship with specialties
    specialties = relationship(
        "Specialty", secondary="doctor_specialties", back_populates="doctors"
    )

    # One-to-many relationship with appointments
    appointments = relationship("Appointment", back_populates="doctor")
