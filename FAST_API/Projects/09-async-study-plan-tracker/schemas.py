from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class CourseCreate(BaseModel):
    user_id: int
    name: str
    description: str


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    description: str
    created_at: datetime


class StudySessionCreate(BaseModel):
    topic: str
    duration_minutes: int = Field(gt=0)
    completed: bool = False


class StudySessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int
    topic: str
    duration_minutes: int = Field(gt=0)
    completed: bool
    created_at: datetime


class CourseSummaryResponse(BaseModel):
    course: str
    total_sessions: int
    completed_sessions: int
    total_minutes: int
