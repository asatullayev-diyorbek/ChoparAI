from django.db import models


class News(models.Model):
    # buni hozirgi versiyada ishlatmadik. agar keyinchalik saytlardan
    # yangiliklar olinadigan bo'lsa ishlatilsa bo'ladi
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
    """
        Kanal haqida ma'lumotlarni saqlovchi model.

        Bu model Telegram kanal(lar)i haqida quyidagi ma'lumotlarni saqlaydi:
        - title: Kanalning to'liq nomi.
        - chat_id: Telegram kanalining noyob identifikatori (chat ID).
        - username: Kanal username (agar mavjud bo‘lsa).
        - is_get_post: Bot ushbu kanaldan xabarlarni olsinmi yo‘qmi belgisi (True/False).
        - created_at: Ushbu kanal bazaga qo‘shilgan sana va vaqt.

        __str__ metodi: Kanal nomi va chat ID ni birlashtirib ko‘rsatadi.

        Meta:
        - verbose_name: Admin interfeysida bitta kanal nomi uchun ko‘rsatiladi.
        - verbose_name_plural: Admin interfeysida ko‘plik shaklda ko‘rsatiladi.
    """
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
    """
        Foydalanuvchining Telegram kanallarini saqlovchi model.

        Maydonlar:
            title (CharField): Kanalning nomi (sarlavhasi).
            chat_id (BigIntegerField): Kanalning noyob Telegram chat ID raqami.
            username (CharField): Kanalga tegishli Telegram username (ixtiyoriy).
            is_send_post (BooleanField): Ushbu kanalga xabar yuborilsinmi yoki yo'q (haqiqat/false).
            created_at (DateTimeField): Kanal bazaga qo‘shilgan vaqti (avtomatik yaratiladi).

        Foydasi:
            - Bu model Telegram orqali xabar yuboriladigan kanallarni boshqarish uchun ishlatiladi.
            - Admin panelda har bir kanalni nomi va ID si bilan ko‘rish imkonini beradi.
    """
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