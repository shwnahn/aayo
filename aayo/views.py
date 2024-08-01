# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
import uuid
from django.views.decorators.http import require_POST
from .crawling import get_starbucks_menu
import json
from django.contrib import messages
from django.core.exceptions import ValidationError

def main(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user_id = request.POST.get('id')
        password = request.POST.get('password')
        cafe = request.POST.get('cafe')

        # 유니크한 URL 생성
        unique_id = str(uuid.uuid4())[:8]

        # Room 모델에 데이터를 저장
        room = Room.objects.create(
            name=name,
            creator=user_id,
            password=password,
            cafe=cafe,
            unique_id=unique_id
        )

        # 방 세부 정보 페이지로 리다이렉트
        return redirect(reverse('room_detail', kwargs={'unique_id': unique_id}))

    return render(request, 'main.html')

def room_detail(request, unique_id):
    room = Room.objects.get(unique_id=unique_id)
    room_link = request.build_absolute_uri(reverse('room_detail', args=[unique_id]))
    return render(request, 'room_detail.html', {'room': room, 'room_link': room_link})

def room_view(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    return render(request, 'room.html', {'room': room})


def enter_room(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    if request.method == 'POST':
        form = EnterRoomForm(request.POST, room=room)
        if form.is_valid():
            guest_name = form.cleaned_data['guest_name']
            request.session['guest_name'] = guest_name
            return redirect('room_menu', unique_id=unique_id)
    else:
        form = EnterRoomForm(room=room)
    
    return render(request, 'room_menu.html', {'room': room, 'form': form})

def room_menu(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    guest_name = request.session.get('guest_name')
    
    # 임시 메뉴 데이터
    dummy_menus = [
        {"name": "아메리카노", "image": "https://example.com/americano.jpg"},
        {"name": "카페라떼", "image": "https://example.com/latte.jpg"},
        {"name": "카푸치노", "image": "https://example.com/cappuccino.jpg"},
    ]
    
    context = {
        'room': room,
        'guest_name': guest_name,
        'menus': dummy_menus,
    }
    return render(request, 'room_menu.html', context)


def confirm_menu(request, unique_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, unique_id=unique_id)
        selected_menus = request.POST.getlist('selected_menus')
        guest_name = request.session.get('guest_name')
        
        if not selected_menus:
            return redirect('room_menu', unique_id=unique_id)
        
        order = GuestOrder.objects.create(
            room=room,
            guest_name=guest_name,
            menus=json.dumps(selected_menus)
        )
        
        return redirect('order_detail', unique_id=unique_id, order_id=order.id)
    
    return redirect('room_menu', unique_id=unique_id)

def order_detail(request, unique_id, order_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    order = get_object_or_404(GuestOrder, id=order_id, room=room)
    
    try:
        selected_menus = json.loads(order.menus)
        # print(selected_menus)
    except json.JSONDecodeError:
        selected_menus = []
    
    context = {
        'room': room,
        'guest_name': order.guest_name,
        'selected_menus': selected_menus,
        'unique_id': unique_id,  # 여기에 unique_id를 추가

    }
    return render(request, 'order_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Room, GuestOrder
import json

def order_total(request, unique_id):
    # 특정 Room 객체를 가져옵니다.
    room = get_object_or_404(Room, unique_id=unique_id)
    
    # 해당 방의 모든 GuestOrder를 가져옵니다.
    guest_orders = GuestOrder.objects.filter(room=room)
    
    all_menus = []
    
    # 각 GuestOrder의 메뉴를 처리합니다.
    for order in guest_orders:
        try:
            menus = json.loads(order.menus)
            all_menus.extend(menus)
        except json.JSONDecodeError:
            continue
    
    # 중복 제거 및 각 메뉴의 주문 횟수를 계산
    menu_counts = {}
    for menu in all_menus:
        if menu in menu_counts:
            menu_counts[menu] += 1
        else:
            menu_counts[menu] = 1
    
    context = {
        'room_name': room.name,
        'menu_counts': menu_counts,
        'total_orders': len(all_menus)
    }
    
    return render(request, 'order_total.html', context)

def reset_order(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    guest_name = request.session.get('guest_name')

    if guest_name:
        # 해당 게스트의 주문을 찾아 삭제
        GuestOrder.objects.filter(room=room, guest_name=guest_name).delete()
        messages.success(request, "기존 주문이 삭제되었습니다. 새로운 메뉴를 선택해주세요.")
    else:
        messages.error(request, "게스트 정보를 찾을 수 없습니다.")

    # 메뉴 선택 페이지로 리다이렉트
    return redirect('room_menu', unique_id=unique_id)