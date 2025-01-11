import enum


# Role Enum
class UserRole(enum.Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"
    PATIENT = "Patient"


# Appointment Status Enum
class AppointmentStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELED = "Canceled"


# Payment Status Enum
class PaymentStatus(enum.Enum):
    COMPLETED = "Completed"
    FAILED = "Failed"
