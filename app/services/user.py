from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.repositories.user import UserRepository
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession, users: UserRepository) -> None:
        self.session = session
        self.users = users

    async def create_user(self, payload: UserCreate):
        existing_user = await self.users.get_by_email(payload.email)
        if existing_user is not None:
            raise EmailAlreadyExistsError(f"user with email '{payload.email}' already exists.")

        user = await self.users.create(email=str(payload.email), full_name=payload.full_name)
        await self.session.commit()
        return user

    async def get_user(self, user_id: uuid.UUID):
        user = await self.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"user '{user_id}' was not found.")
        return user

    async def list_users(self, pagination: PaginationParams) -> PaginatedResponse:
        users = await self.users.list(limit=pagination.limit, offset=pagination.offset)
        total = await self.users.count()
        return PaginatedResponse(
            items=users,
            total=total,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def delete_user(self, user_id: uuid.UUID) -> None:
        user = await self.get_user(user_id)
        await self.users.delete(user)
        await self.session.commit()
