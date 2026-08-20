# Technical Test Report: Job Application Tracker API

**Date & Time:** 2026-08-18  
**API Version:** 1.0.0  
**Environment:** FastAPI with SQLite (`job_tracker.db`)  
**Test Framework:** Starlette TestClient / Python unittest

---

## Executive Summary

All endpoints of the **Job Application Tracker API** were thoroughly tested for standard CRUD operations (Create, Read, Update, Delete) and database integrity. Additionally, sample data was successfully inserted into the database.

**Overall Status:** `PASSED` (15/15 Endpoint Operations Verified)

---

## Endpoint Test Results

### 1. Root & System Health Endpoints
| Endpoint | HTTP Method | Expected Status | Result Status | Status |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `GET` | 200 OK | 200 OK | **PASSED** |
| `/db-check` | `GET` | 200 OK | 200 OK | **PASSED** |

---

### 2. User Management Endpoints (`/users`)
| Endpoint | HTTP Method | Description / Payload | Status |
| :--- | :--- | :--- | :--- |
| `/users` | `POST` | Create User (`Alice Smith`, `Bob Jones`) | **PASSED** |
| `/users` | `GET` | Retrieve list of all users | **PASSED** |
| `/users/{user_id}` | `PUT` | Update user details | **PASSED** |
| `/users/{user_id}` | `DELETE` | Delete temp user & verify 404 on subsequent requests | **PASSED** |

---

### 3. Company Management Endpoints (`/companies`)
| Endpoint | HTTP Method | Description / Payload | Status |
| :--- | :--- | :--- | :--- |
| `/companies` | `POST` | Create Company (`TechCorp`, `DataDynamics`) | **PASSED** |
| `/companies` | `GET` | Retrieve list of all companies | **PASSED** |
| `/companies/{company_id}` | `PUT` | Update company information | **PASSED** |
| `/companies/{company_id}` | `DELETE` | Delete temp company | **PASSED** |

---

### 4. Job Listing Endpoints (`/job_listings`)
| Endpoint | HTTP Method | Description / Payload | Status |
| :--- | :--- | :--- | :--- |
| `/job_listings` | `POST` | Create Job Listing (`Backend Python Engineer`, `Data Scientist`) | **PASSED** |
| `/job_listings` | `GET` | Retrieve list of all job listings | **PASSED** |
| `/job_listings/{job_listing_id}` | `PUT` | Update job listing details | **PASSED** |
| `/job_listings/{job_listing_id}` | `DELETE` | Delete temp job listing | **PASSED** |

---

### 5. Job Application Endpoints (`/job_applications`)
| Endpoint | HTTP Method | Description / Payload | Status |
| :--- | :--- | :--- | :--- |
| `/job_applications` | `POST` | Create Job Application (`Applied`, `Interview Scheduled`) | **PASSED** |
| `/job_applications` | `GET` | Retrieve list of all applications | **PASSED** |
| `/job_applications/{application_id}` | `PUT` | Update application status | **PASSED** |
| `/job_applications/{application_id}` | `DELETE` | Delete temp application | **PASSED** |

---

## Fixes & Schema Adjustments Made

During testing, a schema mismatch was identified in `schemas.py`:
- **Issue:** `JobApplicationResponse` expected a field named `applied_at`, whereas the SQLAlchemy model `models.JobApplication` defined `applied_date`. This caused a `ResponseValidationError` on `POST /job_applications` and `GET /job_applications`.
- **Resolution:** Updated `schemas.py` to use `applied_date: datetime`.

---

## Seeded Sample Data

The following relational sample data is currently active in the SQLite database (`job_tracker.db`):

### Users
1. **Alice Smith** (`alice@example.com`)
2. **Bob Jones** (`bob@example.com`)

### Companies
1. **TechCorp** (Industry: *Software Engineering*, Location: *San Francisco, CA*, Website: *https://techcorp.example.com*)
2. **DataDynamics** (Industry: *Data Analytics*, Location: *New York, NY*, Website: *https://datadynamics.example.com*)

### Job Listings
1. **Backend Python Engineer** (Company: *TechCorp*, Location: *San Francisco, CA*)
2. **Data Scientist** (Company: *DataDynamics*, Location: *New York, NY*)

### Job Applications
1. **User:** Alice Smith → **Job:** Backend Python Engineer (**Status:** `Applied`)
2. **User:** Bob Jones → **Job:** Data Scientist (**Status:** `Interview Scheduled`)

---

## How to Run Tests & Verification

To re-run the automated test suite and seed script at any time, execute:

```bash
python test_runner.py
```
