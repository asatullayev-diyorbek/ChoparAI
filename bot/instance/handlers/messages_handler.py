import pprint

from aiogram.types import Message
from aiogram import Bot
from asgiref.sync import sync_to_async

from bot.instance.handlers.utils import translate_text, extract_url_and_build_button
from bot.models import Channel, MyChannel
from config.settings import USERBOT_CHAT_ID


post_bottom = (
    "📲 Yangiliklar va foydali maslahatlar uchun: \n"
    '<a href="https://t.me/nurinvest">Telegram</a> | '
    '<a href="https://www.instagram.com/nurinvest.uz?igsh=MW53NHk0NnNibXh6bA==">Instagram</a>'
)



@sync_to_async
def get_my_channels():
    return list(MyChannel.objects.filter(is_send_post=True).values_list('chat_id', flat=True))





async def handle_all_messages(message: Message, bot: Bot) -> None:
    if int(USERBOT_CHAT_ID) != message.chat.id:
        return

    if message.forward_from_chat and message.forward_from_chat.type == 'channel':
        is_true = await Channel.objects.filter(is_get_post=True, chat_id=message.forward_from_chat.id).aexists()

        if is_true:
            my_channels = await get_my_channels()
            original_text = message.text or message.caption or ""

            # # Tarjima qilish
            # translated_text = await translate_text(
            #     text=original_text,
            #     source_lang="rus_Cyrl",
            #     target_lang="uzn_Latn",
            #     model="sayqalchi"
            # )

            translated_text = "Test xabarda bu, ekonomichestki"
            for channel_id in my_channels:
                # Media bilanmi yoki faqat matnmi
                if message.photo:
                    # Agar rasmli post bo‘lsa
                    await bot.send_photo(
                        chat_id=channel_id,
                        photo=message.photo[-1].file_id,  # eng yuqori sifatli variant
                        caption=translated_text + "\n\n" + post_bottom,
                        parse_mode='html',
                        reply_markup= await extract_url_and_build_button(message.reply_markup)
                    )
                else:
                    # Oddiy matnli xabar
                    await bot.send_message(
                        chat_id=channel_id,
                        text=translated_text + "\n\n" + post_bottom,
                        parse_mode="html",
                        disable_web_page_preview=True,
                        reply_markup=await extract_url_and_build_button(message.reply_markup)
                    )

            print("✅ Tarjima va yuborish yakunlandi.")

        # pprint.pprint(message.__dict__)