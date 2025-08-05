from aiogram.types import Message
from aiogram import Bot


async def handle_start(message: Message, bot: Bot) -> None:
    """
        /start komandasi kelganda ishga tushuvchi xabarni qayta ishlaydi.

        Foydalanuvchi tomonidan yuborilgan xabarni o‘chirib tashlaydi (agar mumkin bo‘lsa)
        va javoban ikki xabar yuboradi:
            1. "Ishga tayyorman!" — bot ishga tayyorligini bildiradi.
            2. Foydalanuvchining ID'si va bot ID'si ko‘rsatiladi (test/debug maqsadlarida).

        Parametrlar:
            message (Message): Kiruvchi Telegram xabari
            bot (Bot): Aiogram bot obyekti

        Returns:
            None
    """
    await message.answer("Ishga tayyorman!")
    await message.answer(f"{message.from_user.id}   {message.bot.id}")