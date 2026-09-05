import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database import Base, get_db
from main import app

# Setup test async database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True, scope="function")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.anyio
async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/test")
        assert response.status_code == 200
        assert response.json() == {"message": "App is working "}


# ==========================================
# PATIENT TESTS (200, 404, 422)
# ==========================================


@pytest.mark.anyio
async def test_patient_crud_200():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Create Patient (200)
        patient_data = {
            "name": "John Doe",
            "age": 30,
            "gender": "Male",
            "phone": "1234567890",
            "email": "john@example.com",
        }
        res_create = await ac.post("/patients/", json=patient_data)
        assert res_create.status_code == 200
        patient_id = res_create.json()["id"]
        assert res_create.json()["name"] == "John Doe"

        # Get All Patients (200)
        res_list = await ac.get("/patients/")
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # Get Patient By ID (200)
        res_get = await ac.get(f"/patients/{patient_id}")
        assert res_get.status_code == 200
        assert res_get.json()["id"] == patient_id

        # Update Patient (200)
        updated_data = {
            "name": "John Updated",
            "age": 31,
            "gender": "Male",
            "phone": "0987654321",
            "email": "john_updated@example.com",
        }
        res_update = await ac.put(f"/patients/{patient_id}", json=updated_data)
        assert res_update.status_code == 200
        assert res_update.json()["name"] == "John Updated"

        # Delete Patient (200)
        res_delete = await ac.delete(f"/patients/{patient_id}")
        assert res_delete.status_code == 200
        assert res_delete.json() == {
            "detail": f"{patient_id} patient has been deleted"
        }


@pytest.mark.anyio
async def test_patient_404_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res_get = await ac.get("/patients/999")
        assert res_get.status_code == 404
        assert res_get.json() == {"detail": "patient not found"}

        update_data = {
            "name": "Ghost",
            "age": 20,
            "gender": "Other",
            "phone": "0000000000",
            "email": "ghost@example.com",
        }
        res_put = await ac.put("/patients/999", json=update_data)
        assert res_put.status_code == 404
        assert res_put.json() == {"detail": "patient not found"}

        res_del = await ac.delete("/patients/999")
        assert res_del.status_code == 404
        assert res_del.json() == {"detail": "patient not found"}


@pytest.mark.anyio
async def test_patient_422_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Invalid data type (age as string instead of int)
        invalid_data = {
            "name": "Invalid Patient",
            "age": "invalid_age",
            "gender": "Male",
            "phone": "1234567890",
            "email": "invalid@example.com",
        }
        res = await ac.post("/patients/", json=invalid_data)
        assert res.status_code == 422


# ==========================================
# DOCTOR TESTS (200, 404, 422)
# ==========================================


@pytest.mark.anyio
async def test_doctor_crud_200():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Create Doctor (200)
        doctor_data = {
            "name": "Dr. Smith",
            "specialization": "Cardiology",
            "phone": "1112223333",
            "email": "smith@hospital.com",
        }
        res_create = await ac.post("/doctors/", json=doctor_data)
        assert res_create.status_code == 200
        doctor_id = res_create.json()["id"]

        # Get Doctor List (200)
        res_list = await ac.get("/doctors/")
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # Get Doctor by ID (200)
        res_get = await ac.get(f"/doctors/{doctor_id}")
        assert res_get.status_code == 200

        # Update Doctor (200)
        updated_data = {
            "name": "Dr. Smith Jr.",
            "specialization": "Neurology",
            "phone": "1112223333",
            "email": "smith_jr@hospital.com",
        }
        res_update = await ac.put(f"/doctors/{doctor_id}", json=updated_data)
        assert res_update.status_code == 200
        assert res_update.json()["specialization"] == "Neurology"

        # Delete Doctor (200)
        res_delete = await ac.delete(f"/doctors/{doctor_id}")
        assert res_delete.status_code == 200


@pytest.mark.anyio
async def test_doctor_404_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/doctors/999")
        assert res.status_code == 404
        assert res.json() == {"detail": "doctor not found"}


@pytest.mark.anyio
async def test_doctor_422_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Missing required field 'specialization'
        invalid_data = {
            "name": "Dr. Missing Spec",
            "phone": "1234567890",
            "email": "missing@example.com",
        }
        res = await ac.post("/doctors/", json=invalid_data)
        assert res.status_code == 422


# ==========================================
# APPOINTMENT TESTS (200, 404, 422)
# ==========================================


@pytest.mark.anyio
async def test_appointment_crud_200():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # First create patient and doctor
        p_res = await ac.post(
            "/patients/",
            json={
                "name": "Patient One",
                "age": 25,
                "gender": "Female",
                "phone": "123",
                "email": "p1@test.com",
            },
        )
        p_id = p_res.json()["id"]

        d_res = await ac.post(
            "/doctors/",
            json={
                "name": "Doctor One",
                "specialization": "General",
                "phone": "456",
                "email": "d1@test.com",
            },
        )
        d_id = d_res.json()["id"]

        # Create Appointment (200)
        appt_data = {
            "patient_id": p_id,
            "doctor_id": d_id,
            "appointment_date_time": "2026-09-01T10:00:00",
            "reason": "Routine Checkup",
            "status": "Scheduled",
        }
        res_create = await ac.post("/appointments/", json=appt_data)
        assert res_create.status_code == 200
        appt_id = res_create.json()["id"]

        # Get Appointments (200)
        res_list = await ac.get("/appointments/")
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # Get Appointment by ID (200)
        res_get = await ac.get(f"/appointments/{appt_id}")
        assert res_get.status_code == 200

        # Update Appointment (200)
        updated_data = {
            "patient_id": p_id,
            "doctor_id": d_id,
            "appointment_date_time": "2026-09-01T11:00:00",
            "reason": "Followup",
            "status": "Completed",
        }
        res_update = await ac.put(f"/appointments/{appt_id}", json=updated_data)
        assert res_update.status_code == 200
        assert res_update.json()["status"] == "Completed"

        # Delete Appointment (200)
        res_delete = await ac.delete(f"/appointments/{appt_id}")
        assert res_delete.status_code == 200


@pytest.mark.anyio
async def test_appointment_404_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/appointments/999")
        assert res.status_code == 404
        assert res.json() == {"detail": "appointment not found"}


@pytest.mark.anyio
async def test_appointment_404_nonexistent_patient_or_doctor():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Create appointment with non-existent patient
        appt_data = {
            "patient_id": 9999,
            "doctor_id": 1,
            "appointment_date_time": "2026-09-01T10:00:00",
            "reason": "Test",
            "status": "Scheduled",
        }
        res = await ac.post("/appointments/", json=appt_data)
        assert res.status_code == 404
        assert res.json() == {"detail": "patient not found"}


@pytest.mark.anyio
async def test_appointment_422_validation_error():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Invalid datetime format
        invalid_data = {
            "patient_id": 1,
            "doctor_id": 1,
            "appointment_date_time": "not-a-datetime",
            "reason": "Test",
            "status": "Scheduled",
        }
        res = await ac.post("/appointments/", json=invalid_data)
        assert res.status_code == 422
