from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from bot.models import Channel


@csrf_exempt
def channels(request):
    """
        Kanal ro'yxatini yangilovchi HTTP POST endpoint.

        Bu funksiya tashqi manbadan kelayotgan `channel_list` event turidagi JSON so‘rovni qabul qiladi.
        Yangi kanallar ro'yxati bazaga qo‘shiladi yoki yangilanadi, mavjud bo‘lmagan eski kanallar esa o‘chiriladi.

        Faoliyat:
        - So‘rov turi POST bo'lishi kerak.
        - Content-Type `application/json` bo'lishi kerak.
        - JSON ichida `event` qiymati `channel_list` bo‘lishi shart.
        - `channels` nomli ro'yxat bo'lishi va har bir elementda `chat_id` bo'lishi kerak.
        - Har bir kanal bo‘yicha `chat_id`, `title`, `username` ma’lumotlari yangilanadi yoki yangi yozuv yaratiladi.
        - Mavjud, lekin so‘rovda yo‘q bo‘lgan kanallar o‘chiriladi.

        Parametrlar:
        - request (HttpRequest): Django POST so‘rovi. JSON formatda quyidagi ko‘rinishda bo'lishi kerak:
            {
                "event": "channel_list",
                "channels": [
                    {
                        "chat_id": 123456789,
                        "title": "Kanal nomi",
                        "username": "kanal_username"
                    },
                    ...
                ]
            }

        Javoblar:
        - 200 OK: muvaffaqiyatli bajarilgan bo‘lsa:
            {
                "status": "success",
                "received": <yangi/yoki yangilangan kanallar soni>,
                "deleted": <o‘chirilgan kanallar soni>
            }

        - 400 Bad Request: noto‘g‘ri ma’lumot yuborilgan bo‘lsa:
            {
                "error": "Izoh",
                "details": "Xatolik haqida batafsil (agar mavjud bo‘lsa)"
            }

        - 405 Method Not Allowed: agar POST bo‘lmasa

        Misol:
            curl -X POST https://<domain>/channels/ \
                -H "Content-Type: application/json" \
                -d '{
                    "event": "channel_list",
                    "channels": [
                        {"chat_id": "123456", "title": "Test", "username": "test_channel"}
                    ]
                }'
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        # Kontent turi tekshiruv
        if request.content_type != "application/json":
            return JsonResponse({"error": "Invalid Content-Type, expected application/json"}, status=400)

        # JSON decode
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON decode error", "details": str(e)}, status=400)

        # Event tekshiruvi
        if data.get("event") != "channel_list":
            return JsonResponse({"error": "Unsupported event", "received_event": data.get("event")}, status=400)

        new_channels = data.get("channels", [])
        if not isinstance(new_channels, list):
            return JsonResponse({"error": "channels must be a list"}, status=400)

        # Bazadagi va kelgan chat_id lar
        existing_ids = set(Channel.objects.values_list('chat_id', flat=True))
        incoming_ids = set()

        for ch in new_channels:
            raw_id = ch["chat_id"]
            chat_id = raw_id if str(raw_id).startswith("-100") else int(f"-100{raw_id}")
            title = ch.get("title", "")
            username = ch.get("username", "")
            if not chat_id:
                return JsonResponse({"error": "channel missing chat_id", "channel": ch}, status=400)

            incoming_ids.add(chat_id)
            Channel.objects.update_or_create(
                chat_id=chat_id,
                defaults={
                    "title": title,
                    "username": username
                }
            )

        # Eski kanallarni o'chirish
        to_delete = existing_ids - incoming_ids
        Channel.objects.filter(chat_id__in=to_delete).delete()

        return JsonResponse({
            "status": "success",
            "received": len(new_channels),
            "deleted": len(to_delete)
        })

    except Exception as e:
        # Har qanday boshqa xatolik uchun
        return JsonResponse({"error": "Unhandled exception", "details": str(e)}, status=400)






