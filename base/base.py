from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import your models here
from apps.appointments.models import Appointment
from apps.doctor.models import Specialty, DoctorSpecialty, Doctor
from apps.patient.models import Patient
from apps.user.models import User
