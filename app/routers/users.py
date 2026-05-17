from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies import get_project_service, get_user_service
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.project import ProjectResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.project import ProjectService
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "email already exists"}},
)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await service.create_user(payload)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={404: {"description": "user not found"}},
)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await service.get_user(user_id)


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UserService = Depends(get_user_service),
) -> PaginatedResponse[UserResponse]:
    return await service.list_users(PaginationParams(limit=limit, offset=offset))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "user not found"}},
)
async def delete_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> Response:
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{user_id}/projects",
    response_model=list[ProjectResponse],
    responses={404: {"description": "user not found"}},
)
async def list_user_projects(
    user_id: uuid.UUID,
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    return await service.list_user_projects(user_id)
