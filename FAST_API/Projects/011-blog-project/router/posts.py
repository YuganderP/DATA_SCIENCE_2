from fastapi import Depends
from database import get_db

from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Post, User
from schemas import PostCreate, PostResponse
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.execute(select(Post))
    result = posts.scalars().all()
    return result


@router.post("/", response_model=PostResponse)
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    data = db.execute(select(User).filter(post.user_id == User.id))
    user = data.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail={"content": "user not found"})
    new_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    data = db.execute(select(Post).filter(post_id == Post.id))
    post = data.scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail={"content": "user not found"})
    return post
