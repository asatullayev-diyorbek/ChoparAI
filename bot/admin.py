from django.contrib import admin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin

from bot.models import News, Channel, MyChannel

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy maʼlumotlar', {'fields': ('first_name', 'last_name', 'email')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'is_send', 'created_at')
    list_filter = ('category', 'is_send', 'created_at')
    search_fields = ('title', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ('title', 'chat_id', 'username', 'is_get_post', 'created_at')
    list_filter = ('is_get_post', 'created_at')
    search_fields = ('title', 'username', 'chat_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(MyChannel)
class ChannelAdmin(ModelAdmin):
    list_display = ('title', 'chat_id', 'username', 'is_send_post', 'created_at')
    list_filter = ('is_send_post', 'created_at')
    search_fields = ('title', 'username', 'chat_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)