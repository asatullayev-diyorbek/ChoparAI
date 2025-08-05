from django.urls import path
from bot.views.webhook.get_webhook import handle_updates
from bot.views.userbot.views import channels


urlpatterns = [
    # webhook uchun
    path("webhook/<str:bot_id>/updates", handle_updates),

    # userbot kanallar ro'yxati uchun
    path('userbot/updates/channels/', channels)

]
