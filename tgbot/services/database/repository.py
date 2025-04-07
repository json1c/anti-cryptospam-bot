from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot.services.database.engine import Base, engine
from tgbot.services.database.models.banned_user import BannedUser
from tgbot.services.database.models.joined_user import JoinedUser


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
    
    async def get_joined_user(self, telegram_id: int, chat_id: int) -> JoinedUser | None:
        async with self.get_session() as session:
            result = await session.execute(
                select(JoinedUser)
                .where(
                    and_(
                        JoinedUser.telegram_id == telegram_id,
                        JoinedUser.chat_id == chat_id
                    )
                )
            )
        
            return result.scalar_one_or_none()
    
    async def create_joined_user(self, telegram_id: int, chat_id: int):
        async with self.get_session() as session:
            joined_user = JoinedUser(
                telegram_id=telegram_id,
                chat_id=chat_id
            )

            session.add(joined_user)
            await session.commit()

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
