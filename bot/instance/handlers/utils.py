from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientSession

from config.settings import TILMOCH_TOKEN


async def translate_text(text, source_lang="rus_Cyrl", target_lang="uzn_Latn", model="sayqalchi"):
    """
        Matnni berilgan manba tilidan maqsadli tilga tarjima qiladi (Tahrirchi API orqali).

        Ushbu funksiya Tahrirchi tarjima xizmati API'si orqali matnni asinxron tarzda
        tarjima qiladi. Tarjimada ishlatiladigan til kodi va model nomi ixtiyoriy parametrlar
        sifatida uzatiladi.

        Parametrlar:
            text (str): Tarjima qilinadigan matn.
            source_lang (str): Manba tilining kodi (standart: "rus_Cyrl").
            target_lang (str): Maqsad tilining kodi (standart: "uzn_Latn").
            model (str): Tarjimada ishlatiladigan model nomi (standart: "sayqalchi").

        Returns:
            str: Tarjima qilingan matn (yoki xatolik bo‘lsa asl matn qaytariladi).
    """
    url = "https://websocket.tahrirchi.uz/translate-v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": TILMOCH_TOKEN
    }
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": model
    }

    async with ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("translated_text", text)
            else:
                print("❌ Tarjima xatosi:", await response.text())
                return text


async def extract_url_and_build_button(reply_markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup | None:
    """
        InlineKeyboardMarkup ichidan URL mavjud bo‘lgan tugmani ajratib oladi va yagona "Batafsil/Подробнее" tugmasini yaratadi.

        Agar mavjud reply_markup ichida URL mavjud bo‘lgan tugma topilsa,
        u holda yangi InlineKeyboardMarkup yaratilib, unda faqat bitta universal
        tugma ("Batafsil/Подробнее") URL bilan birga qaytariladi.

        Aks holda (ya'ni URL topilmasa yoki reply_markup mavjud bo‘lmasa) None qaytariladi.

        Parametrlar:
            reply_markup (InlineKeyboardMarkup): Asl inline tugmalar markup'i

        Returns:
            InlineKeyboardMarkup | None: URL bo‘yicha yagona tugma markup'i yoki hech narsa (None)
    """
    if not reply_markup:
        return None

    for row in reply_markup.inline_keyboard:
        for button in row:
            if button.url:
                return InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Batafsil/Подробнее ", url=button.url)]
                    ]
                )
    return None