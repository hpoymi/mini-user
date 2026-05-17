from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ProjectNotFoundError, UserNotFoundError
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository
from app.schemas.project import ProjectCreate


class ProjectService:
    def __init__(
        self,
        session: AsyncSession,
        projects: ProjectRepository,
        users: UserRepository,
    ) -> None:
        self.session = session
        self.projects = projects
        self.users = users

    async def create_project(self, payload: ProjectCreate):
        user = await self.users.get_by_id(payload.owner_id)
        if user is None:
            raise UserNotFoundError(f"owner '{payload.owner_id}' was not found.")

        project = await self.projects.create(
            name=payload.name,
            description=payload.description,
            owner_id=payload.owner_id,
        )
        await self.session.commit()
        return project

    async def get_project(self, project_id: uuid.UUID):
        project = await self.projects.get_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"project '{project_id}' was not found.")
        return project

    async def list_user_projects(self, user_id: uuid.UUID):
        user = await self.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"user '{user_id}' was not found.")
        return await self.projects.list_by_owner(user_id)
