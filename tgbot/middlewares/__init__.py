from aiogram import Dispatcher

from tgbot.config import Config


def register_middlewares(dp: Dispatcher, config: Config):
    from . import repository

    repository.register_middleware(dp=dp)
