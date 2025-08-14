import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async  # IMPORTANT for SQLite safety
from django.contrib.auth.models import User
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Reject anonymous sockets (no session)
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        other_username = self.scope["url_route"]["kwargs"]["room_name"]
        me = self.scope["user"].username

        # Canonical room key from the two usernames
        self.room_key = Room.dm_room_name(me, other_username)
        self.group_name = f"chat_{self.room_key}"

        # Make sure the room exists and both participants are added
        await self.ensure_room(me, other_username)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except Exception:
            return

        msg = (data.get("message") or "").strip()
        if not msg:
            return

        sender = self.scope["user"]

        # Persist first (so history reload works even if broadcast fails)
        await self.create_message(sender.id, self.room_key, msg)

        # Broadcast to the room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",  # MUST match method name below
                "message": msg,
                "sender": sender.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    # --------- DB helpers (run in thread with correct connection handling) ---------

    @database_sync_to_async
    def ensure_room(self, u1: str, u2: str):
        key = Room.dm_room_name(u1, u2)
        room, _ = Room.objects.get_or_create(name=key)
        users = list(User.objects.filter(username__in=[u1, u2]))
        if users:
            room.participants.add(*users)
        return room

    @database_sync_to_async
    def create_message(self, sender_id: int, room_key: str, content: str):
        room = Room.objects.get(name=room_key)
        return Message.objects.create(room=room, sender_id=sender_id, content=content)
