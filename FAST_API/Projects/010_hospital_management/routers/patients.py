from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Patient
from schemas import PatientCreate, PatientResponse
from exceptions import PatientNotFoundException


router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        phone=patient.phone,
        email=patient.email,
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    result = db.execute(select(Patient))
    patients = result.scalars().all()

    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Patient).filter(Patient.id == patient_id))

    patient = result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)
):
    result = db.execute(select(Patient).filter(Patient.id == patient_id))

    patient_db = result.scalars().first()

    if patient_db is None:
        raise PatientNotFoundException

    patient_db.name = patient.name
    patient_db.age = patient.age
    patient_db.gender = patient.gender
    patient_db.phone = patient.phone
    patient_db.email = patient.email

    db.commit()
    db.refresh(patient_db)

    return patient_db


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Patient).filter(Patient.id == patient_id))

    patient = result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    db.delete(patient)
    db.commit()

    return JSONResponse(
        status_code=200, content={"detail": f"{patient_id} patient has been deleted"}
    )
