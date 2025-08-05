import os

from dotenv import load_dotenv
from telethon import TelegramClient, events
import requests
from telethon.tl.types import PeerChannel

from config.settings import dotenv_path

# --- Telegram API ma'lumotlari ---
load_dotenv(dotenv_path, override=True)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
DJANGO_ENDPOINT = os.getenv("BOT_HOST") + "/bot/userbot/updates/"
SESSION_NAME = "userbot"

BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")

# --- Client yaratish ---
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)



@client.on(events.NewMessage)
async def handle_message(event: events.newmessage.NewMessage.Event):
    """
        Telegram mijozidan yangi xabarlarni tutib oluvchi asinxron funksiyasi.

        Ushbu funksiya ikkita asosiy vazifani bajaradi:
        1. Agar foydalanuvchi "/channels" buyrug'ini yuborgan bo‘lsa:
            - Telegramdagi barcha kanallar ro‘yxatini (chat_id, nomi, username) to‘playdi.
            - Ushbu ro‘yxatni JSON formatida Django serveriga POST so‘rovi orqali yuboradi.
            - Xabarni yuborish holatini terminalga chiqaradi.

        2. Aks holda (ya'ni, oddiy kanal xabari bo‘lsa):
            - Xabar faqat kanal turiga mansub bo‘lsa tekshiriladi (`PeerChannel`).
            - Kanal xabari aniqlansa, uni admin Telegram botiga (`BOT_CHAT_ID`) forward qiladi.
            - Forward muvaffaqiyatli yoki xatolik bilan yakunlansa, u terminalga chiqadi.

        Xatoliklar turli bosqichlarda aniqlanadi va konsolga chiqariladi:
        - Django serverga so‘rov yuborishda
        - Kanal xabarini forward qilishda
        - Event obyekti bilan ishlashda

    """
    try:
        text = event.raw_text.strip()

        # /channels buyrug‘i
        if text == "/channels":
            dialogs = await client.get_dialogs()
            channels = [
                {
                    "chat_id": dialog.entity.id,
                    "title": dialog.name,
                    "username": getattr(dialog.entity, 'username', None),
                }
                for dialog in dialogs
                if dialog.is_channel
            ]

            payload = {
                "event": "channel_list",
                "channels": channels
            }
            response = requests.post(DJANGO_ENDPOINT + 'channels/', json=payload, timeout=5)
            print("✅ Kanal ro'yxati yuborildi:", response.status_code)
        else:
            try:
                # Faqat kanaldan kelgan xabarlar
                if isinstance(event.message.peer_id, PeerChannel):
                    try:
                        # Kanal IDdan input_entity yaratish
                        from_peer = await client.get_input_entity(event.chat_id)

                        await client.forward_messages(
                            entity=int(BOT_CHAT_ID),
                            messages=event.message.id,
                            from_peer=from_peer  # kanal entity
                        )
                        print("✅ Kanal xabari forward qilindi.")
                    except Exception as e:
                        print("❌ Forward xatolik:", e)
                else:
                    print("ℹ️ Bu xabar kanal emas, o'tkazib yuborildi.")
            except Exception as e:
                print("❌ Umumiy xatolik:", e)

    except Exception as e:
        print("❌ Xatolik (message):", e)



if __name__ == "__main__":
    print("📡 Userbot ishga tushdi...")
    client.start()
    client.run_until_disconnected()
