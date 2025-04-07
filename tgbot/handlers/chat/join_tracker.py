from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from tgbot.services.database.repository import Repository

router = Router()

@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def handle_joined_user(chat_member: ChatMemberUpdated, repo: Repository):
    telegram_id = chat_member.new_chat_member.user.id
    chat_id = chat_member.chat.id

    if not await repo.get_joined_user(telegram_id, chat_id):
        await repo.create_joined_user(
            telegram_id=telegram_id,
            chat_id=chat_id
        )
