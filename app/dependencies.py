from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository
from app.services.project import ProjectService
from app.services.user import UserService


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repo = UserRepository(session)
    return UserService(session=session, users=user_repo)


async def get_project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    return ProjectService(
        session=session,
        projects=project_repo,
        users=user_repo,
    )
