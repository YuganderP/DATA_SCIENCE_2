from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from database import get_db
from model import StudySession
import schemas
from exceptions import CourseNotFoundException

router = APIRouter(prefix="/sessions", tags=["session"])


@router.get("/{session_id}", response_model=schemas.StudySessionResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StudySession)
        .options(selectinload(StudySession.course))
        .filter(StudySession.id == session_id)
    )
    session = result.scalars().first()
    if session is None:
        raise CourseNotFoundException()  ## raising this exception on temp basis
    return session


@router.put("/{session_id}", response_model=schemas.StudySessionResponse)
async def update_session(
    session_id: int,
    session_data: schemas.StudySessionCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudySession).filter(StudySession.id == session_id)
    )

    session = result.scalars().first()

    if session is None:
        raise CourseNotFoundException()

    session.topic = session_data.topic
    session.duration_minutes = session_data.duration_minutes
    session.completed = session_data.completed

    await db.commit()
    await db.refresh(session)

    return session
