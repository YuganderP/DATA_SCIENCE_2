from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from model import User, Course, StudySession
import schemas
from exceptions import UserNotFoundException, CourseNotFoundException

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=schemas.CourseResponse)
async def add_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == course.user_id))
    user_id_check = result.scalars().first()
    if user_id_check is None:
        raise UserNotFoundException(course.user_id)
    new_course = Course(
        user_id=course.user_id, name=course.name, description=course.description
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@router.get("/", response_model=list[schemas.CourseResponse])
async def get_courses(db: AsyncSession = Depends(get_db)):
    courses = await db.execute(select(Course))
    courses = courses.scalars().all()
    return courses


@router.get("/{course_id}", response_model=schemas.CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.execute(select(Course).filter(course_id == Course.id))
    course = course.scalars().first()
    if course is None:
        raise CourseNotFoundException()
    return course


@router.delete("/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.execute(select(Course).filter(course_id == Course.id))
    course = course.scalars().first()
    if course is None:
        raise CourseNotFoundException()
    db.delete(course)
    await db.commit()
    return {"message": f"{course_id} has been deleted"}


@router.get("/{course_id}/sessions", response_model=list[schemas.StudySessionResponse])
async def get_study_sessions(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course_check = result.scalars().first()
    if course_check is None:
        raise CourseNotFoundException()
    result = await db.execute(
        select(StudySession).filter(StudySession.course_id == course_id)
    )
    study_sessions = result.scalars().all()
    return study_sessions


@router.post("/{course_id}/sessions", response_model=schemas.StudySessionResponse)
async def create_study_session(
    course_id: int,
    session: schemas.StudySessionCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course_check = result.scalars().first()
    if course_check is None:
        raise CourseNotFoundException()
    new_session = StudySession(
        course_id=course_id,
        topic=session.topic,
        duration_minutes=session.duration_minutes,
        completed=session.completed,
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session
