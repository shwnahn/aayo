from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Room  # Room 모델을 import. 아직 생성하지 않았다면 나중에 추가하세요.

def room_detail(request, unique_id):
    try:
        room = Room.objects.get(unique_id=unique_id)
    except Room.DoesNotExist:
        return render(request, '404.html', {'message': '방을 찾을 수 없습니다.'}, status=404)

    context = {
        'room': room,
        'share_link': request.build_absolute_uri(),
    }

    return render(request, 'room_detail.html', context)

def share_link(request, unique_id):
    if request.method == 'POST' and request.is_ajax():
        link = request.build_absolute_uri(reverse('room_detail', args=[unique_id]))
        return JsonResponse({'status': 'success', 'link': link})
    return JsonResponse({'status': 'error'}, status=400)