from django.contrib import admin

from .models import Subscriptions, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'date_joined',
        'first_name',
        'last_name',
        'role',
    )
    exclude = (
        'last_login',
        'groups',
        'user_permissions',
        'is_staff',
        'is_superuser'
    )
    list_filter = ('email', 'username')
    search_fields = ('username',)


@admin.register(Subscriptions)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('author',)
