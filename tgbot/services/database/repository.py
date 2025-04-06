from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot.services.database.engine import Base, engine
from tgbot.services.database.models.banned_user import BannedUser


class Repository:
    def __init__(self):
        self.session = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session() as session:
            yield session

    async def init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_banned_user(self, telegram_id: int):
        async with self.get_session() as session:
            user = BannedUser(telegram_id=telegram_id)

            session.add(user)
            await session.commit()
    
    async def get_banned_users_count(self) -> int:
        async with self.get_session() as session:
            stmt = (
                select(func.count())
                .select_from(BannedUser)
            )

            return await session.scalar(stmt)        
