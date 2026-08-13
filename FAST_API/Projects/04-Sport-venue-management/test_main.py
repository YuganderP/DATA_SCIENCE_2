import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Use a separate SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sports_venue.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Re-create tables in the test database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clean tables before each test to have isolation
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


# ==========================================
# VENUE TESTS
# ==========================================

def test_create_venue():
    response = client.post(
        "/venues",
        json={"name": "Stadium A", "location": "City Center", "description": "Large stadium"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Stadium A"
    assert data["location"] == "City Center"
    assert data["description"] == "Large stadium"
    assert "id" in data

def test_get_venues():
    # Create two venues
    client.post(
        "/venues",
        json={"name": "Venue 1", "location": "Loc 1", "description": "Desc 1"},
    )
    client.post(
        "/venues",
        json={"name": "Venue 2", "location": "Loc 2", "description": "Desc 2"},
    )

    response = client.get("/venues")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Venue 1"
    assert data[1]["name"] == "Venue 2"

def test_get_venue_by_id():
    # Create venue
    res = client.post(
        "/venues",
        json={"name": "Venue A", "location": "Loc A", "description": "Desc A"},
    )
    venue_id = res.json()["id"]

    # Retrieve
    response = client.get(f"/venues/{venue_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Venue A"

    # Non-existent
    response_404 = client.get("/venues/999")
    assert response_404.status_code == 404
    assert "no venue with given venue id found" in response_404.json()["detail"]["Message"]

def test_update_venue():
    res = client.post(
        "/venues",
        json={"name": "Old Venue", "location": "Old Loc", "description": "Old Desc"},
    )
    venue_id = res.json()["id"]

    response = client.put(
        f"/venues/{venue_id}",
        json={"name": "New Venue", "location": "New Loc", "description": "New Desc"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Venue"

    # Update non-existent
    response_404 = client.put(
        "/venues/999",
        json={"name": "New Venue", "location": "New Loc", "description": "New Desc"},
    )
    assert response_404.status_code == 404

def test_delete_venue():
    res = client.post(
        "/venues",
        json={"name": "To Delete", "location": "Loc", "description": "Desc"},
    )
    venue_id = res.json()["id"]

    response = client.delete(f"/venues/{venue_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    # Delete non-existent
    response_404 = client.delete("/venues/999")
    assert response_404.status_code == 404


# ==========================================
# USER TESTS
# ==========================================

def test_create_user():
    # Needs a venue first
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    response = client.post(
        "/users",
        json={"name": "John Doe", "email": "john@example.com", "role": "admin", "venue_id": venue_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["venue_id"] == venue_id

def test_get_users():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    client.post(
        "/users",
        json={"name": "User 1", "email": "u1@example.com", "role": "member", "venue_id": venue_id},
    )
    client.post(
        "/users",
        json={"name": "User 2", "email": "u2@example.com", "role": "member", "venue_id": venue_id},
    )

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user_by_id():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User A", "email": "ua@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "User A"

    response_404 = client.get("/users/999")
    assert response_404.status_code == 404

def test_update_user():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User Old", "email": "old@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"name": "User New", "email": "new@example.com", "role": "admin", "venue_id": venue_id},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "User New"
    assert response.json()["role"] == "admin"

    response_404 = client.put(
        "/users/999",
        json={"name": "User New", "email": "new@example.com", "role": "admin", "venue_id": venue_id},
    )
    assert response_404.status_code == 404

def test_delete_user():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "To Delete", "email": "del@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    response_404 = client.delete("/users/999")
    assert response_404.status_code == 404


# ==========================================
# FACILITY TESTS
# ==========================================

def test_create_facility():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    response = client.post(
        "/facilities",
        json={
            "sport_type": "Tennis",
            "description": "Outdoor clay court",
            "name": "Court 1",
            "venue_id": venue_id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sport_type"] == "Tennis"
    assert data["venue_id"] == venue_id

def test_get_facilities():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )

    response = client.get("/facilities")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_facility_by_id():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    response = client.get(f"/facilities/{facility_id}")
    assert response.status_code == 200
    assert response.json()["sport_type"] == "Tennis"

    response_404 = client.get("/facilities/999")
    assert response_404.status_code == 404

def test_update_facility():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    response = client.put(
        f"/facilities/{facility_id}",
        json={
            "sport_type": "Basketball",
            "description": "Indoor court",
            "name": "Court 2",
            "venue_id": venue_id,
        },
    )
    assert response.status_code == 200
    assert response.json()["sport_type"] == "Basketball"

    response_404 = client.put(
        "/facilities/999",
        json={
            "sport_type": "Basketball",
            "description": "Indoor court",
            "name": "Court 2",
            "venue_id": venue_id,
        },
    )
    assert response_404.status_code == 404

def test_delete_facility():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    response = client.delete(f"/facilities/{facility_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    response_404 = client.delete("/facilities/999")
    assert response_404.status_code == 404


# ==========================================
# BOOKING TESTS
# ==========================================

def test_create_booking():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User", "email": "u@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    response = client.post(
        "/bookings",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "12:00",
            "status": "Confirmed",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["facility_id"] == facility_id
    assert data["booking_date"] == "2026-08-15"

def test_get_bookings():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User", "email": "u@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    client.post(
        "/bookings",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "12:00",
            "status": "Confirmed",
        },
    )

    response = client.get("/bookings")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_booking_by_id():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User", "email": "u@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    b_res = client.post(
        "/bookings",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "12:00",
            "status": "Confirmed",
        },
    )
    booking_id = b_res.json()["id"]

    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "Confirmed"

    response_404 = client.get("/bookings/999")
    assert response_404.status_code == 404
    assert "no booking with given booking found" in response_404.json()["detail"]

def test_update_booking():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User", "email": "u@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    b_res = client.post(
        "/bookings",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "12:00",
            "status": "Pending",
        },
    )
    booking_id = b_res.json()["id"]

    response = client.put(
        f"/bookings/{booking_id}",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "13:00",
            "status": "Confirmed",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Confirmed"
    assert response.json()["end_time"] == "13:00"

    response_404 = client.put(
        "/bookings/999",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "13:00",
            "status": "Confirmed",
        },
    )
    assert response_404.status_code == 404

def test_delete_booking():
    v_res = client.post(
        "/venues",
        json={"name": "V", "location": "L", "description": "D"},
    )
    venue_id = v_res.json()["id"]

    u_res = client.post(
        "/users",
        json={"name": "User", "email": "u@example.com", "role": "member", "venue_id": venue_id},
    )
    user_id = u_res.json()["id"]

    f_res = client.post(
        "/facilities",
        json={"sport_type": "Tennis", "description": "Court", "name": "C1", "venue_id": venue_id},
    )
    facility_id = f_res.json()["id"]

    b_res = client.post(
        "/bookings",
        json={
            "user_id": user_id,
            "facility_id": facility_id,
            "booking_date": "2026-08-15",
            "start_time": "10:00",
            "end_time": "12:00",
            "status": "Confirmed",
        },
    )
    booking_id = b_res.json()["id"]

    response = client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]

    response_404 = client.delete("/bookings/999")
    assert response_404.status_code == 404
