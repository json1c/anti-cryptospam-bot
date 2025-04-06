from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.services.check_message import check_text
from tgbot.services.database.repository import Repository

router = Router()

@router.message(Command("/pidors"))
async def handle_users_count(message: Message, repo: Repository):
    users_count = await repo.get_banned_users_count()

    await message.reply(f"🏳️‍🌈 Заблокировано спамеров: {users_count}")


@router.message(F.forward_from_chat)
async def handle_forwarded_message(
    message: Message,
    bot: Bot,
    repo: Repository
):
    message_text = message.text or message.caption

    if not message_text:
        return
    
    result = check_text(message_text)

    if result:
        found, keyword, confident = result

        await bot.ban_chat_member(message.chat.id, message.from_user.id)
        await message.delete()

        await repo.create_banned_user(telegram_id=message.from_user.id)

        return await message.answer(
            (
                f"🐓 ID <code>{message.from_user.id}</code> заблокирован навсегда за отправку спама.\n\n"
                
                f"(cid: <code>{message.forward_from_chat.id}</code>, search: <code>{keyword}</code>, found: {found}, уверенность: {confident}%)\n\n"

                f"<i>🏳️‍🌈 Всего заблокировано: /pidors</i>"
            ),
            parse_mode="html"
        )
