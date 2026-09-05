from fastapi import FastAPI, Request
from router.posts import router as post_router
from router.users import router as user_router
from fastapi.staticfiles import StaticFiles
from database import Base, db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import get_db, db
from sqlalchemy.orm import Session
from fastapi import Depends
from models import User, Post
from sqlalchemy import select

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=db)


@app.get("/")
def show_post(request: Request, db: Session = Depends(get_db)):
    data = db.execute(select(Post))
    posts = data.scalars().all()
    return templates.TemplateResponse("home.html", {"request": request, "posts": posts})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
