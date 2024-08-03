from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
from django.utils import timezone

def room_detail(request, unique_id):
    try:
        room = Room.objects.get(unique_id=unique_id)
    except Room.DoesNotExist:
        return HttpResponse("방을 찾을 수 없습니다.", status=404)

    context = {
        'room': room,
        'share_link': request.build_absolute_uri(),
        'created_at': timezone.localtime(room.created_at).strftime("%Y-%m-%d %H:%M:%S")
    }

    return render(request, 'room_detail.html', context)