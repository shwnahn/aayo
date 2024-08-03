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

def room_menu(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    
    if request.method == 'POST':
        if 'guest_name' in request.POST:
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
        order_total = sum(menu['price'] for menu in menus)
        total += order_total
        orders_details.append({
            'guest_name': order.guest_name,
            'menus': menus,
            'total': order_total
        })
    
    context = {
        'room': room,
        'orders_details': orders_details,
        'total': total,
    }
    return render(request, 'room_orders.html', context)