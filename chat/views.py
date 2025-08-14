from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from .models import Room, Message


@login_required
def chat_room(request, room_name: str):
    """
    `room_name` is the OTHER user's username (DM).
    """
    other = get_object_or_404(User, username=room_name)
    if other.id == request.user.id:
        return redirect("home")

    # Ensure room exists and both are participants
    key = Room.dm_room_name(request.user.username, other.username)
    room, _ = Room.objects.get_or_create(name=key)
    room.participants.add(request.user, other)

    # History
    chats = Message.objects.filter(room=room).select_related("sender")

    # Build sidebar list (what your template expects: `partners_info`)
    # All users except me, with a last-message preview if we have a room
    others = User.objects.exclude(id=request.user.id).order_by("username")
    partners_info = []
    for u in others:
        rk = Room.dm_room_name(request.user.username, u.username)
        last = Message.objects.filter(room__name=rk).order_by("-timestamp").first()
        partners_info.append({"user": u, "last": last})

    return render(request, "chat/chat.html", {
        "room_name": other.username,   # the DM partner
        "chats": chats,                # existing messages
        "partners_info": partners_info # sidebar items your template loops over
    })
