from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import CallbackQuery, Message, Update

from tgbot.services.database.repository import Repository


class DbRepoMiddleware(BaseMiddleware):
    def __init__(self):
        self.repo = Repository()

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        data["repo"] = self.repo

        await handler(event, data)


def register_middleware(dp: Dispatcher):
    db_middleware = DbRepoMiddleware()
    dp.update.middleware(db_middleware)
