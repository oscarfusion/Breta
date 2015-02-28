from django.contrib import admin

from .models import Message, MessageFile, MessageRecipient


class MessageFileInline(admin.StackedInline):
    extra = 1
    model = MessageFile


class MessageRecipientInline(admin.StackedInline):
    extra = 1
    model = MessageRecipient


class MessageAdmin(admin.ModelAdmin):
    inlines = [MessageFileInline, MessageRecipientInline]
    list_display = ('type', 'subject', 'sender', 'created_at', 'sent_at',)


admin.site.register(Message, MessageAdmin)
