from django.contrib import admin

from .models import Event, EventNotification


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['datetime', 'confidence', 'meta', 'camera', 'detector']


@admin.register(EventNotification)
class EventNotificationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'is_read']
