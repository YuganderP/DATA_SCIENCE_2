from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Patient
from schemas import PatientCreate, PatientResponse
from exceptions import PatientNotFoundException


router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        phone=patient.phone,
        email=patient.email,
    )

    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)

    return new_patient


@router.get("/", response_model=list[PatientResponse])
async def get_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient))
    patients = result.scalars().all()

    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))

    patient = result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int, patient: PatientCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))

    patient_db = result.scalars().first()

    if patient_db is None:
        raise PatientNotFoundException

    patient_db.name = patient.name
    patient_db.age = patient.age
    patient_db.gender = patient.gender
    patient_db.phone = patient.phone
    patient_db.email = patient.email

    await db.commit()
    await db.refresh(patient_db)

    return patient_db


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).filter(Patient.id == patient_id))

    patient = result.scalars().first()

    if patient is None:
        raise PatientNotFoundException

    await db.delete(patient)
    await db.commit()

    return JSONResponse(
        status_code=200, content={"detail": f"{patient_id} patient has been deleted"}
    )
