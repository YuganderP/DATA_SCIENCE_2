from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate, UserResponse, PostCreate, PostResponse
from sqlalchemy import select
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.execute(select(User))
    result = users.scalars().all()
    return result


@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="email registered")

    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    users = db.execute(select(User).filter(user_id == User.id))
    result = users.scalars().first()
    if result is None:
        raise HTTPException(status_code=404, detail={"connect": "user not found"})

    return result
