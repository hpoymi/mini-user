from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import func, select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, *, email: str, full_name: str) -> User:
        user = User(email=email, full_name=full_name)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(self, *, limit: int, offset: int) -> list[User]:
        result = await self.session.execute(
            select(User).order_by(User.full_name, User.email).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(User))
        return int(result.scalar_one())

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
