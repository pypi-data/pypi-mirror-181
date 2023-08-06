from django.contrib import admin

from unicef_notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'sent_recipients')
    raw_id_fields = ('sent_email', )
