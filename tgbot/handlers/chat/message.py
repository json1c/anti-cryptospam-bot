from datetime import datetime, timezone

from aiogram import Bot, F, Router
from aiogram.types import Message

from tgbot.services.database.repository import Repository
from tgbot.services.detectors.check_crypto_spam import check_text
from tgbot.services.detectors.check_work_spam import work_spam_probability

router = Router()


@router.message()
async def handle_default_message(
    message: Message,
    bot: Bot,
    repo: Repository
):
    if not message.text:
        return

    joined_user = await repo.get_joined_user(
        telegram_id=message.from_user.id,
        chat_id=message.chat.id
    )

    is_recent_join = False
    seconds_passed = None

    if joined_user and joined_user.created_at:
        now = datetime.now(timezone.utc)

        if joined_user.created_at.tzinfo is None:
            created_at = joined_user.created_at.replace(tzinfo=timezone.utc)
        else:
            created_at = joined_user.created_at

        diff = now - created_at
        seconds_passed = diff.total_seconds()

        if seconds_passed <= 120:
            is_recent_join = True

    message_text = message.text.lower()

    probability = work_spam_probability(message_text)

    if is_recent_join:
        probability = min(probability + 20, 100)
    
    if probability >= 80:
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
        await message.delete()
        await repo.create_banned_user(telegram_id=message.from_user.id)

        joined_status = "Да" if is_recent_join else "Нет"

        await message.answer(
            (
                f"🐓 ID <code>{message.from_user.id}</code> заблокирован навсегда за отправку спама.\n\n"

                f"(Зашел недавно? {joined_status}, прошло после захода: {seconds_passed} сек., уверенность в спаме: {probability}%)\n\n"

                f"<i>🏳️‍🌈 Всего заблокировано: /pidors</i>"
            ),
            parse_mode="html"
        )


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
