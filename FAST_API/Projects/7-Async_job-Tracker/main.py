from fastapi import FastAPI, Depends
from app import models
from contextlib import asynccontextmanager
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session, select, selectinload
from app.database import get_db
from schemas import CompanyCreate, CompanyResponse, JobListingCreate, JobListingResponse
from schemas import (
    JobApplicationCreate,
    JobApplicationResponse,
    UserCreate,
    UserResponse,
)
from fastapi import status, HTTPException
from sqlalchemy.exc import IntegrityError

app = FastAPI(
    title="Job Application Tracker",
    description="A multi user job appication tracking system",
    version="1.0.0",
)

# CREATE A LIFESPAN FUNCTION  FOR STARTUP AND END


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


inspector = inspect(engine)
# print(inspector.get_table_names())
# print(inspector.get_columns("companies"))
# print(inspector.get_pk_constraint("companies"))
# print(inspector.get_unique_constraints("companies"))


# print(inspector.get_unique_constraints("job_applications"))
# print(inspector.get_foreign_keys("job_applications"))
print(inspector.get_unique_constraints("job_applications"))


@app.get("/")
def root():
    return {"message": "Job appication tracker API"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"message": "Db session created successfully "}


@app.post("/companies", response_model=CompanyResponse)
def add_company(company: CompanyCreate, db: Session = Depends(get_db)):
    new_company = models.Company(
        name=company.name,
        industry=company.industry,
        location=company.location,
        website=company.website,
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@app.get("/companies", response_model=list[CompanyResponse])
async def get_companies(db: AsyncSession = Depends(get_db)):
    # companies = db.query(models.Company).all()
    companies = await db.execute(
        select(models.Company).options(selectinload(models.Company.job_listings))
    )
    companies = companies.scalars().all()
    return companies


@app.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int, company: CompanyCreate, db: Session = Depends(get_db)
):
    existing_company = (
        db.query(models.Company).filter(models.Company.id == company_id).first()
    )

    if existing_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no company found with company id",
        )

    existing_company.name = company.name
    existing_company.industry = company.industry
    existing_company.location = company.location
    existing_company.website = company.website

    db.commit()
    db.refresh(existing_company)
    return existing_company


@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no company found with company id",
        )

    db.delete(company)
    db.commit()
    return {"message": f" company with {company_id} has been deleted "}


@app.post("/job_listings", response_model=JobListingResponse)
def add_job_listing(job_lising: JobListingCreate, db: Session = Depends(get_db)):
    company_check = (
        db.query(models.Company)
        .filter(models.Company.id == job_lising.company_id)
        .first()
    )
    if company_check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="please enter existing company id",
        )
    new_job_listing = models.JobListing(
        company_id=job_lising.company_id,
        title=job_lising.title,
        description=job_lising.description,
        location=job_lising.location,
        posted_date=job_lising.posted_date,
        closing_date=job_lising.closing_date,
    )
    db.add(new_job_listing)
    db.commit()
    db.refresh(new_job_listing)
    return new_job_listing


@app.get("/job_listings", response_model=list[JobListingResponse])
async def get_job_listings(db: AsyncSession = Depends(get_db)):
    data = await db.execute(
        select(models.JobListing).options(selectinload(models.JobListing.company))
    )
    data = data.scalars().all()
    return data


@app.put("/job_listings/{job_listing_id}", response_model=JobListingResponse)
def update_job_listing(
    job_listing_id: int, job_lising: JobListingCreate, db: Session = Depends(get_db)
):
    existing_job_listing = (
        db.query(models.JobListing)
        .filter(models.JobListing.id == job_listing_id)
        .first()
    )

    if existing_job_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no job found with job listing id",
        )

    if (
        job_lising.closing_date is not None
        and job_lising.closing_date <= job_lising.posted_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid closing date"
        )

    existing_job_listing.company_id = job_lising.company_id
    existing_job_listing.title = job_lising.title
    existing_job_listing.description = job_lising.description
    existing_job_listing.location = job_lising.location
    existing_job_listing.posted_date = job_lising.posted_date
    existing_job_listing.closing_date = job_lising.closing_date

    db.commit()
    db.refresh(existing_job_listing)
    return existing_job_listing


@app.delete("/job_listings/{job_listing_id}")
def delete_job_listing(job_listing_id: int, db: Session = Depends(get_db)):
    job_listing = (
        db.query(models.JobListing)
        .filter(models.JobListing.id == job_listing_id)
        .first()
    )
    if job_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no company found with company id",
        )

    db.delete(job_listing)
    db.commit()
    return {"message": f" job with {job_listing_id} has been deleted "}


@app.post("/job_applications", response_model=JobApplicationResponse)
def add_job_application(
    application: JobApplicationCreate, db: Session = Depends(get_db)
):
    check_user_id = (
        db.query(models.User).filter(models.User.id == application.user_id).first()
    )
    check_job_listing = (
        db.query(models.JobListing)
        .filter(models.JobListing.id == application.job_listing_id)
        .first()
    )

    if check_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid user id"
        )
    if check_job_listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please enter Valid job listing id ",
        )
    new_application = models.JobApplication(
        user_id=application.user_id,
        job_listing_id=application.job_listing_id,
        status=application.status,
    )

    db.add(new_application)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user has already applied to the job",
        )
    db.refresh(new_application)
    return new_application


@app.get("/job_applications", response_model=list[JobApplicationResponse])
def get_job_applications(db: Session = Depends(get_db)):
    applications = db.query(models.JobApplication).all()

    return applications


@app.put("/job_applications/{application_id}", response_model=JobApplicationResponse)
def update_job_application(
    application_id: int,
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
):
    existing_application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if existing_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no job application found with application id",
        )

    existing_application.user_id = application.user_id
    existing_application.job_listing_id = application.job_listing_id
    existing_application.status = application.status

    db.commit()
    db.refresh(existing_application)

    return existing_application


@app.delete("/job_applications/{application_id}")
def delete_job_application(application_id: int, db: Session = Depends(get_db)):
    application = (
        db.query(models.JobApplication)
        .filter(models.JobApplication.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no job application found with application id",
        )

    db.delete(application)
    db.commit()

    return {"message": f"job application with {application_id} has been deleted"}


@app.post("/users", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no user found with user id",
        )

    existing_user.name = user.name
    existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)

    return existing_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no user found with user id",
        )

    db.delete(user)
    db.commit()

    return {"message": f"user with {user_id} has been deleted"}
