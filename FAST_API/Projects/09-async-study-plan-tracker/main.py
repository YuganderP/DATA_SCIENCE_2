from fastapi import FastAPI, Request
from database import engine

from exceptions import UserNotFoundException
from fastapi.responses import JSONResponse


from contextlib import asynccontextmanager
from database import create_tables


from routers.users import router as users_router
from routers.courses import router as courses_router
from routers.studysessions import router as sessions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(courses_router)
app.include_router(sessions_router)


@app.exception_handler(UserNotFoundException)
def user_not_found(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404, content={"message": f"user{exc.user_id} not found"}
    )


@app.get("/")
def home():
    return {"message": "Application started"}
