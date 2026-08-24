from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from model import User, Course
import schemas
from exceptions import UserNotFoundException

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserResponse, status_code=201)
async def add_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/", response_model=list[schemas.UserResponse], status_code=200)
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    users = users.scalars().all()
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse, status_code=200)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise UserNotFoundException(user_id)
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise UserNotFoundException(user_id)
    db.delete(user)
    await db.commit()
    return {"message": f"user with {user_id} has been deleted"}


@router.get("/{user_id}/courses", response_model=list[schemas.CourseResponse])
async def get_user_courses(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise UserNotFoundException(user_id)
    result = await db.execute(select(Course).filter(Course.user_id == user_id))
    courses = result.scalars().all()
    return courses
