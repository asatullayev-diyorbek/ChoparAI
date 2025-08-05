from django.db import models

class News(models.Model):
    title = models.CharField(
        max_length=500,
        verbose_name='Sarlavha'
    )
    url = models.URLField(
        verbose_name='Havola'
    )
    image_url = models.URLField(
        verbose_name='Rasm havolasi'
    )
    category = models.CharField(
        max_length=100,
        verbose_name='Kategoriya'
    )
    is_send = models.BooleanField(
        default=False,
        verbose_name='Yuborilganmi?'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Tavsif')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )

    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Channel(models.Model):
    title = models.CharField(max_length=500, verbose_name="Kanal nomi")
    chat_id = models.BigIntegerField(verbose_name="Kanal ID")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    is_get_post = models.BooleanField(default=False, verbose_name="Xabar olinsinmi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqt")

    def __str__(self):
        return f"{self.title} ({self.chat_id})"

    class Meta:
        verbose_name = "Kanal"
        verbose_name_plural = "Kanallar"


class MyChannel(models.Model):
    title = models.CharField(max_length=500, verbose_name="Kanal nomi")
    chat_id = models.BigIntegerField(verbose_name="Kanal ID")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    is_send_post = models.BooleanField(default=False, verbose_name="Xabar yuborilsinmi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqt")

    def __str__(self):
        return f"{self.title} ({self.chat_id})"

    class Meta:
        verbose_name = "Mening kanalim"
        verbose_name_plural = "Mening kanallarim"