from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.services.database.repository import Repository

router = Router()

@router.message(Command("pidors"))
async def handle_users_count(message: Message, repo: Repository):
    users_count = await repo.get_banned_users_count()

    await message.reply(f"🏳️‍🌈 Заблокировано спамеров: {users_count}")
