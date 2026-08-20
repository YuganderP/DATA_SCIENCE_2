from fastapi import FastAPI, Request
from database import engine, Base
from model import User, StudySession, Course
from exceptions import UserNotFoundException, CourseNotFoundException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from database import get_db
import schemas

app = FastAPI()


@app.exception_handler(UserNotFoundException)
def user_not_found(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404, content={"message": f"user{exc.user_id} not found"}
    )


@app.exception_handler(CourseNotFoundException)
def course_not_found(request: Request, exc: CourseNotFoundException):
    return JSONResponse(status_code=404, content={"message": "course not found"})


Base.metadata.create_all(engine)


@app.get("/")
def home():
    return {"message": "Application started"}


@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[schemas.UserResponse], status_code=200)
def get_users(db: Session = Depends(get_db)):
    users = db.execute(select(User))
    users = users.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=schemas.UserResponse, status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    if user is None:
        raise UserNotFoundException(user_id)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id))
    user = user.scalars().first()
    if user is None:
        raise UserNotFoundException(user_id)
    db.delete(user)
    db.commit()
    return {"message": f"user with {user_id} has been deleted"}


@app.post("/courses", response_model=schemas.CourseResponse)
def add_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    user_id_check = (
        db.execute(select(User).filter(User.id == course.user_id)).scalars().first()
    )
    if user_id_check is None:
        raise UserNotFoundException(course.user_id)
    new_course = Course(
        user_id=course.user_id, name=course.name, description=course.description
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get("/courses", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.execute(select(Course))
    courses = courses.scalars().all()
    return courses


@app.get("/courses/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.execute(select(Course).filter(course_id == Course.id))
    course = course.scalars().first()
    if course is None:
        raise CourseNotFoundException()
    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.execute(select(Course).filter(course_id == Course.id))
    course = course.scalars().first()
    if course is None:
        raise CourseNotFoundException()
    db.delete(course)
    db.commit()
    return {"message": f"{course_id} has been deleted"}


@app.get("/users/{user_id}/courses", response_model=list[schemas.CourseResponse])
def get_user_courses(user_id: int, db: Session = Depends(get_db)):
    user_id_check = (
        db.execute(select(User).filter(User.id == user_id)).scalars().first()
    )
    if user_id_check is None:
        raise UserNotFoundException(user_id)
    courses = (
        db.execute(select(Course).filter(Course.user_id == user_id)).scalars().all()
    )
    return courses
