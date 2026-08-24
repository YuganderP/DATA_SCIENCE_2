from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: EmailStr


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date_time: datetime
    reason: str
    status: str


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date_time: datetime
    reason: str
    status: str
    model_config = ConfigDict(from_attributes=True)
