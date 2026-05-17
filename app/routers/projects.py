from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status

from app.dependencies import get_project_service
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "owner not found"}},
)
async def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return await service.create_project(payload)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    responses={404: {"description": "project not found"}},
)
async def get_project(
    project_id: uuid.UUID,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return await service.get_project(project_id)
