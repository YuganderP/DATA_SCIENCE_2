from fastapi import FastAPI
from database import Base, engine
from routers import patients
from routers import appointments
from routers import doctors
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import (
    DoctorNotFoundException,
    PatientNotFoundException,
    AppointmentNotFoundException,
)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(doctors.router)


@app.exception_handler(PatientNotFoundException)
def patient_not_found_handler(request: Request, exc: PatientNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "patient not found"})


@app.exception_handler(DoctorNotFoundException)
def doctor_not_found_handler(request: Request, exc: DoctorNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "doctor not found"})


@app.exception_handler(AppointmentNotFoundException)
def appointment_not_found_handler(request: Request, exc: AppointmentNotFoundException):
    return JSONResponse(status_code=404, content={"detail": "appointment not found"})


@app.get("/test")
def test():
    return {"message": "App is working "}
