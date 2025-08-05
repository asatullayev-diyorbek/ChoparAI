from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from bot.instance.handlers.command_handler import handle_start
from bot.instance.handlers.messages_handler import handle_all_messages

# Bot webhook uchun funksiyalarni register qilish
webhook_dp = Dispatcher()
webhook_dp.message.register(handle_start, CommandStart())  # /start

webhook_dp.message.register(handle_all_messages)


async def feed_update(token: str, update: dict):
    try:
        webhook_book = Bot(token=token)
        aiogram_update = types.Update(**update)
        await webhook_dp.feed_update(bot=webhook_book, update=aiogram_update)
    finally:
        await webhook_book.session.close()