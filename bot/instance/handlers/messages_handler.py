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
    """
        is_send_post=True bo‘lgan kanallar uchun chat_id lar ro‘yxatini qaytaradi.

        Ushbu funksiya MyChannel modelidan faqat post yuborilishi kerak bo‘lgan
        kanallarni tanlab oladi va ularning chat_id larini ro‘yxat shaklida qaytaradi.
        @sync_to_async dekoratori orqali asinxron funksiyalar ichida ishlatilishi mumkin.

        Returns:
            list: chat_id lar ro‘yxati.
    """
    return list(MyChannel.objects.filter(is_send_post=True).values_list('chat_id', flat=True))


async def handle_all_messages(message: Message, bot: Bot) -> None:
    """
        Kiruvchi xabarni qayta ishlaydi va kerakli kanallarga avtomatik yuboradi.

        Ushbu funksiya foydalanuvchidan kelgan xabarni tekshiradi, agar xabar
        `forward_from_chat` orqali yuborilgan bo‘lsa va kanal ruxsat etilgan bo‘lsa,
        xabar sarlavhasi tarjima qilinadi va ro‘yxatdagi barcha kanallarga yuboriladi.

        Shuningdek, quyidagi filtrlar qo‘llaniladi:
            - Faqat belgilangan USERBOT_CHAT_ID dan kelgan xabarlar qabul qilinadi
            - "Trade Watcher" kanalidan kelgan postlar faqat "JUST IN" bo‘lsa yuboriladi
            - #реклама bo‘lgan xabarlar yuborilmaydi

        Tarjima qoidalari:
            - Sarlavha rus tilidan o‘zbek tiliga tarjima qilinadi
            - Agar "JUST IN" bo‘lsa, o‘zbekchadan yana rus tiliga qayta tarjima qilinadi

        Tarjima qilingan xabar matni ikki tilda (🇷🇺 va 🇺🇿) formatlanadi
        va `post_bottom` bilan yakunlanadi.

        Media mavjud bo‘lsa, rasm bilan birga yuboriladi, aks holda matn sifatida yuboriladi.

        Parametrlar:
            message (Message): Kiruvchi Telegram xabari
            bot (Bot): Aiogram bot obyekti

        Returns:
            None
    """
    if int(USERBOT_CHAT_ID) != message.chat.id:
        return

    if message.forward_from_chat and message.forward_from_chat.type == 'channel':
        try:
            is_true = await Channel.objects.filter(is_get_post=True, chat_id=message.forward_from_chat.id).aexists()

            if is_true:
                my_channels = await get_my_channels()
                original_text = message.html_text or message.caption or ""

                if message.forward_from_chat.title == 'Trade Watcher' and not "JUST IN" in original_text:
                    return

                if "#реклама" in original_text:
                    return

                # 2 yoki undan ko‘p yangi qator (abzats) bo‘yicha bo‘lish
                paragraphs = original_text.strip().split('\n\n')

                # Birinchi abzats — sarlavha sifatida
                headline = paragraphs[0] if paragraphs else ""



                # # Test uchun
                # translated_text = "Test xabarda bu, ekonomichestki"

                # # Tarjima qilish
                translated_text = await translate_text(
                    text=headline,
                    source_lang="rus_Cyrl",
                    target_lang="uzn_Latn",
                    model="sayqalchi"
                )

                translated_ru = None
                if "JUST IN" in headline:
                    translated_ru = await translate_text(
                        text=translated_text,
                        source_lang="eng_Latn",
                        target_lang="rus_Cyrl",
                        model="sayqalchi"
                    )

                uzb_text = translated_text
                rus_text = translated_ru if translated_ru else headline

                message_text = (
                    f"🇷🇺\n"
                    f"{rus_text}\n\n"
                    f"🇺🇿\n"
                    f"{uzb_text}\n\n"
                    f"{post_bottom}"
                )

                for channel_id in my_channels:
                    # Media bilanmi yoki faqat matnmi
                    if message.photo:
                        # Agar rasmli post bo‘lsa
                        await bot.send_photo(
                            chat_id=channel_id,
                            photo=message.photo[-1].file_id,  # eng yuqori sifatli variant
                            caption=message_text,
                            parse_mode='html',
                            reply_markup= await extract_url_and_build_button(message.reply_markup)
                        )
                    else:
                        # Oddiy matnli xabar
                        await bot.send_message(
                            chat_id=channel_id,
                            text=message_text,
                            parse_mode="html",
                            disable_web_page_preview=True,
                            reply_markup=await extract_url_and_build_button(message.reply_markup)
                        )

                print("✅ Tarjima va yuborish yakunlandi.")
        except Exception as e:
            print(f"handle_all_messages Error: {e}")
