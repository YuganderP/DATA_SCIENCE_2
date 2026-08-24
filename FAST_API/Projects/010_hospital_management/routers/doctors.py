from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Doctor
from schemas import DoctorCreate, DoctorResponse
from exceptions import DoctorNotFoundException


router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        phone=doctor.phone,
        email=doctor.email,
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    result = db.execute(select(Doctor))
    doctors = result.scalars().all()

    return doctors


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Doctor).filter(Doctor.id == doctor_id))

    doctor = result.scalars().first()

    if doctor is None:
        raise DoctorNotFoundException

    return doctor


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int, doctor_data: DoctorCreate, db: Session = Depends(get_db)
):
    result = db.execute(select(Doctor).filter(Doctor.id == doctor_id))

    doctor = result.scalars().first()

    if doctor is None:
        raise DoctorNotFoundException

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.phone = doctor_data.phone
    doctor.email = doctor_data.email

    db.commit()
    db.refresh(doctor)

    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Doctor).filter(Doctor.id == doctor_id))

    doctor = result.scalars().first()

    if doctor is None:
        raise DoctorNotFoundException

    db.delete(doctor)
    db.commit()

    return JSONResponse(
        status_code=200, content={"detail": f"{doctor_id} doctor has been deleted"}
    )
