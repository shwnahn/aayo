# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Room, GuestOrder
from django.urls import reverse
import json
import random
import string

def generate_unique_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def main(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        creator = request.POST.get('creator')
        password = request.POST.get('password')
        cafe = request.POST.get('cafe')
        
        unique_id = generate_unique_id()
        while Room.objects.filter(unique_id=unique_id).exists():
            unique_id = generate_unique_id()
        
        new_room = Room.objects.create(
            name=name,
            creator=creator,
            password=password,
            cafe=cafe,
            unique_id=unique_id
        )
        return redirect('room_detail', unique_id=new_room.unique_id)
    return render(request, 'main.html')

def room_detail(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    context = {
        'room': room,
    }
    return render(request, 'room_detail.html', context)

from django.contrib import messages

def room_menu(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'reset_order':
            # 주문 초기화 로직
            guest_name = request.session.get('guest_name')
            if guest_name:
                GuestOrder.objects.filter(room=room, guest_name=guest_name).delete()
                del request.session['guest_name']
                messages.success(request, '주문이 초기화되었습니다.')
            return redirect('room_menu', unique_id=unique_id)
        
        elif 'guest_name' in request.POST:
            # 게스트 이름 저장
            guest_name = request.POST.get('guest_name')
            request.session['guest_name'] = guest_name
            return JsonResponse({'success': True})
        
        elif 'menus' in request.POST:
            # 메뉴 주문 처리
            guest_name = request.session.get('guest_name')
            if not guest_name:
                return JsonResponse({'error': 'Guest name not found'}, status=400)
            
            menus = json.loads(request.POST.get('menus'))
            
            if not menus:
                return JsonResponse({'error': 'No menus selected'}, status=400)
            
            # 주문 저장
            GuestOrder.objects.create(
                room=room,
                guest_name=guest_name,
                menus=json.dumps(menus)
            )
            
            return JsonResponse({'success': True, 'redirect_url': reverse('room_orders', args=[unique_id])})
    
    # GET 요청 처리
    guest_name = request.session.get('guest_name')
    
    # 메뉴 데이터 (실제로는 크롤링이나 데이터베이스에서 가져와야 함)
    menus = [
        {'id': 1, 'name': '아메리카노', 'price': 4500, 'description': '깔끔한 에스프레소와 물의 조화'},
        {'id': 2, 'name': '카페라떼', 'price': 5000, 'description': '부드러운 우유와 에스프레소의 만남'},
        {'id': 3, 'name': '카푸치노', 'price': 5000, 'description': '우유 거품이 풍성한 커피'},
        # ... 더 많은 메뉴 항목 ...
    ]
    
    context = {
        'room': room,
        'guest_name': guest_name,
        'menus': menus,
    }
    return render(request, 'room_menu.html', context)

def room_orders(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    guest_orders = GuestOrder.objects.filter(room=room)
    
    orders_details = []
    total = 0
    for order in guest_orders:
        menus = json.loads(order.menus)
        order_total = 0
        order_menus = []
        for menu in menus:
            menu_id = menu['id']
            options = menu['options']
            # 여기서 menu_id를 사용하여 실제 메뉴 정보를 조회해야 합니다.
            # 예: menu_info = Menu.objects.get(id=menu_id)
            menu_info = next((m for m in MENUS if m['id'] == int(menu_id)), None)
            if menu_info:
                price = menu_info['price']
                # 옵션에 따른 가격 조정 로직을 여기에 추가할 수 있습니다.
                order_total += price
                order_menus.append({
                    'name': menu_info['name'],
                    'price': price,
                    'size': options['size'],
                    'sugar': options['sugar'],
                    'ice': options['ice']
                })
        total += order_total
        orders_details.append({
            'guest_name': order.guest_name,
            'menus': order_menus,
            'total': order_total
        })
    
    context = {
        'room': room,
        'orders_details': orders_details,
        'total': total,
    }
    return render(request, 'room_orders.html', context)

# 임시로 메뉴 정보를 저장 (실제로는 데이터베이스에서 가져와야 함)
MENUS = [
    {'id': 1, 'name': '아메리카노', 'price': 4500, 'description': '깔끔한 에스프레소와 물의 조화'},
    {'id': 2, 'name': '카페라떼', 'price': 5000, 'description': '부드러운 우유와 에스프레소의 만남'},
    {'id': 3, 'name': '카푸치노', 'price': 5000, 'description': '우유 거품이 풍성한 커피'},
]