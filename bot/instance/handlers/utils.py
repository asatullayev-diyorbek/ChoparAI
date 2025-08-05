import pprint

import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientSession

from config.settings import TILMOCH_TOKEN


async def translate_text(text, source_lang="rus_Cyrl", target_lang="uzn_Latn", model="sayqalchi"):
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