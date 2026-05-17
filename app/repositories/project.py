from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select

from app.models.project import Project
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    async def create(self, *, name: str, description: Optional[str], owner_id: uuid.UUID) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        return await self.session.get(Project, project_id)

    async def list_by_owner(self, owner_id: uuid.UUID) -> list[Project]:
        result = await self.session.execute(
            select(Project).where(Project.owner_id == owner_id).order_by(Project.name, Project.id)
        )
        return list(result.scalars().all())
