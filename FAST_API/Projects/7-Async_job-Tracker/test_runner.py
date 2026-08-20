import unittest
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine
from datetime import date

# Reset database for clean test run
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Job appication tracker API"}

def test_db_check():
    response = client.get("/db-check")
    assert response.status_code == 200
    assert response.json() == {"message": "Db session created successfully "}

def test_endpoints_and_seed_data():
    # 1. Test Users Endpoints
    # Create User 1
    u1_payload = {"name": "Alice Smith", "email": "alice@example.com"}
    res = client.post("/users", json=u1_payload)
    assert res.status_code == 200, res.text
    u1_data = res.json()
    u1_id = u1_data["id"]

    # Create User 2
    u2_payload = {"name": "Bob Jones", "email": "bob@example.com"}
    res = client.post("/users", json=u2_payload)
    assert res.status_code == 200
    u2_data = res.json()
    u2_id = u2_data["id"]

    # Create Temp User for Update and Delete tests
    u_temp_payload = {"name": "Temp User", "email": "temp@example.com"}
    res = client.post("/users", json=u_temp_payload)
    assert res.status_code == 200
    u_temp_id = res.json()["id"]

    # Get Users
    res = client.get("/users")
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 3

    # Update User
    res = client.put(f"/users/{u_temp_id}", json={"name": "Temp User Updated", "email": "temp_updated@example.com"})
    assert res.status_code == 200
    assert res.json()["name"] == "Temp User Updated"

    # Delete User
    res = client.delete(f"/users/{u_temp_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]

    # Verify Delete 404
    res = client.delete(f"/users/{u_temp_id}")
    assert res.status_code == 404

    # 2. Test Companies Endpoints
    c1_payload = {
        "name": "TechCorp",
        "industry": "Software Engineering",
        "location": "San Francisco, CA",
        "website": "https://techcorp.example.com"
    }
    res = client.post("/companies", json=c1_payload)
    assert res.status_code == 200
    c1_id = res.json()["id"]

    c2_payload = {
        "name": "DataDynamics",
        "industry": "Data Analytics",
        "location": "New York, NY",
        "website": "https://datadynamics.example.com"
    }
    res = client.post("/companies", json=c2_payload)
    assert res.status_code == 200
    c2_id = res.json()["id"]

    c_temp_payload = {
        "name": "TempCo",
        "industry": "Testing",
        "location": "Remote",
        "website": None
    }
    res = client.post("/companies", json=c_temp_payload)
    assert res.status_code == 200
    c_temp_id = res.json()["id"]

    # Get Companies
    res = client.get("/companies")
    assert res.status_code == 200
    assert len(res.json()) >= 3

    # Update Company
    res = client.put(f"/companies/{c_temp_id}", json={
        "name": "TempCo Updated",
        "industry": "Testing Updated",
        "location": "Remote",
        "website": "https://tempco.example.com"
    })
    assert res.status_code == 200
    assert res.json()["name"] == "TempCo Updated"

    # Delete Company
    res = client.delete(f"/companies/{c_temp_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]

    # 3. Test Job Listings Endpoints
    j1_payload = {
        "company_id": c1_id,
        "title": "Backend Python Engineer",
        "description": "Develop FastAPI microservices and manage databases.",
        "location": "San Francisco, CA",
        "posted_date": str(date.today()),
        "closing_date": "2026-12-31"
    }
    res = client.post("/job_listings", json=j1_payload)
    assert res.status_code == 200
    j1_id = res.json()["id"]

    j2_payload = {
        "company_id": c2_id,
        "title": "Data Scientist",
        "description": "Build ML models and analyze data pipelines.",
        "location": "New York, NY",
        "posted_date": str(date.today()),
        "closing_date": None
    }
    res = client.post("/job_listings", json=j2_payload)
    assert res.status_code == 200
    j2_id = res.json()["id"]

    j_temp_payload = {
        "company_id": c1_id,
        "title": "QA Engineer",
        "description": "Automated testing.",
        "location": "Remote",
        "posted_date": str(date.today()),
        "closing_date": None
    }
    res = client.post("/job_listings", json=j_temp_payload)
    assert res.status_code == 200
    j_temp_id = res.json()["id"]

    # Get Job Listings
    res = client.get("/job_listings")
    assert res.status_code == 200
    assert len(res.json()) >= 3

    # Update Job Listing
    res = client.put(f"/job_listings/{j_temp_id}", json={
        "company_id": c1_id,
        "title": "Senior QA Engineer",
        "description": "Automated and performance testing.",
        "location": "Remote",
        "posted_date": str(date.today()),
        "closing_date": "2026-11-30"
    })
    assert res.status_code == 200
    assert res.json()["title"] == "Senior QA Engineer"

    # Delete Job Listing
    res = client.delete(f"/job_listings/{j_temp_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]

    # 4. Test Job Applications Endpoints
    a1_payload = {
        "user_id": u1_id,
        "job_listing_id": j1_id,
        "status": "Applied"
    }
    res = client.post("/job_applications", json=a1_payload)
    assert res.status_code == 200
    a1_id = res.json()["id"]

    a2_payload = {
        "user_id": u2_id,
        "job_listing_id": j2_id,
        "status": "Interview Scheduled"
    }
    res = client.post("/job_applications", json=a2_payload)
    assert res.status_code == 200
    a2_id = res.json()["id"]

    a_temp_payload = {
        "user_id": u1_id,
        "job_listing_id": j2_id,
        "status": "Draft"
    }
    res = client.post("/job_applications", json=a_temp_payload)
    assert res.status_code == 200
    a_temp_id = res.json()["id"]

    # Get Job Applications
    res = client.get("/job_applications")
    assert res.status_code == 200
    assert len(res.json()) >= 3

    # Update Job Application
    res = client.put(f"/job_applications/{a_temp_id}", json={
        "user_id": u1_id,
        "job_listing_id": j2_id,
        "status": "Rejected"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "Rejected"

    # Delete Job Application
    res = client.delete(f"/job_applications/{a_temp_id}")
    assert res.status_code == 200
    assert "deleted" in res.json()["message"]

if __name__ == "__main__":
    test_root()
    test_db_check()
    test_endpoints_and_seed_data()
    print("ALL ENDPOINT TESTS PASSED SUCCESSFULLY!")
