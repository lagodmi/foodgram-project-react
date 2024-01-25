from django.contrib import admin

from .models import User, Follower


@admin.register(User)
class AthUserAdmin(admin.ModelAdmin):

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # def display_subscribers(self, obj):
    #     subscribers = Follower.objects.filter(user=obj)
    #     return ', '.join([subscriber.user for subscriber in subscribers])

    # display_subscribers.short_description = 'Subscribers'

    # list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'display_subscribers')
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    fields = ('username', 'email', 'first_name', 'last_name')
    list_display_links = ('id', 'username',)
    list_filter = ('username', 'email')


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscriber')

