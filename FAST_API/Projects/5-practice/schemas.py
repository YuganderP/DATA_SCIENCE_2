from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from datetime import datetime, date
from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"
    ACCEPTED = "Accepted"


class CompanyCreate(BaseModel):
    name: str
    industry: str
    location: str
    website: str | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: str
    location: str
    website: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobListingCreate(BaseModel):
    company_id: int
    title: str
    description: str
    location: str
    posted_date: date
    closing_date: date | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.closing_date is not None and self.closing_date <= self.posted_date:
            raise ValueError("closing date must be after posted date")

        return self


class JobListingResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    location: str
    posted_date: date
    closing_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobApplicationCreate(BaseModel):
    user_id: int
    job_listing_id: int
    status: ApplicationStatus


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_listing_id: int
    status: ApplicationStatus
    applied_date: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
