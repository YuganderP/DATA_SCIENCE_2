from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Appointment, Patient, Doctor
from schemas import AppointmentCreate, AppointmentResponse
from exceptions import (
    AppointmentNotFoundException,
    PatientNotFoundException,
    DoctorNotFoundException,
)


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    patient_result = db.execute(
        select(Patient).filter(Patient.id == appointment.patient_id)
    )

    patient = patient_result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    doctor_result = db.execute(
        select(Doctor).filter(Doctor.id == appointment.doctor_id)
    )

    doctor = doctor_result.scalars().first()

    if doctor is None:
        raise DoctorNotFoundException

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date_time=appointment.appointment_date_time,
        reason=appointment.reason,
        status=appointment.status,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    result = db.execute(select(Appointment))
    appointments = result.scalars().all()

    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Appointment).filter(Appointment.id == appointment_id))

    appointment = result.scalars().first()

    if appointment is None:
        raise AppointmentNotFoundException

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    result = db.execute(select(Appointment).filter(Appointment.id == appointment_id))

    appointment = result.scalars().first()

    if appointment is None:
        raise AppointmentNotFoundException

    patient_result = db.execute(
        select(Patient).filter(Patient.id == appointment_data.patient_id)
    )

    patient = patient_result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    doctor_result = db.execute(
        select(Doctor).filter(Doctor.id == appointment_data.doctor_id)
    )

    doctor = doctor_result.scalars().first()

    if doctor is None:
        raise DoctorNotFoundException

    appointment.patient_id = appointment_data.patient_id
    appointment.doctor_id = appointment_data.doctor_id
    appointment.appointment_date_time = appointment_data.appointment_date_time
    appointment.reason = appointment_data.reason
    appointment.status = appointment_data.status

    db.commit()
    db.refresh(appointment)

    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Appointment).filter(Appointment.id == appointment_id))

    appointment = result.scalars().first()

    if appointment is None:
        raise AppointmentNotFoundException

    db.delete(appointment)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": f"{appointment_id} appointment has been deleted"},
    )
