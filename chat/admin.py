from django.contrib import admin
from .models import Room, Message

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "get_participants")
    search_fields = ("name", "participants__username")

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "room", "short_content", "timestamp")
    list_filter = ("room", "timestamp")
    search_fields = ("sender__username", "content")

    def short_content(self, obj):
        return obj.content[:50] 
    short_content.short_description = "Content"
