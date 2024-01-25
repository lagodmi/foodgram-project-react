from django.contrib import admin

from .models import User, Follower


@admin.register(User)
class AthUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    fields = ('username', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'username',)
    list_filter = ('username', 'email')


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscriber')
