# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.template.loader import render_to_string
import json
import random
import string
from django.template.loader import render_to_string
import logging

def generate_unique_id(): # 방 뒤에 생성되는 유니크 url을 생성하는 함수이다.
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def index(request): # 메인 화면 렌더링 함수
    return render(request, 'index.html')

def room(request): # 방 생성 함수 
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password') # 숨기기 처리 해놓음
        cafe_name = request.POST.get('cafe')
        cafe = Cafe.objects.get(name=cafe_name)
        unique_id = generate_unique_id()
        while Room.objects.filter(unique_id=unique_id).exists():
            unique_id = generate_unique_id()
        new_room = Room.objects.create(
            name=name,
            password=password,
            cafe=cafe,
            unique_id=unique_id,
            
        )
        # 추가된 부분: 새 방을 생성할 때 게스트 이름 초기화
        if 'guest_name' in request.session:
            del request.session['guest_name']
            
        return redirect('room_detail', unique_id=new_room.unique_id)
    
    ctx = {
        'cafes': Cafe.objects.all(),
    }
    return render(request, 'room.html', ctx)

def room_detail(request, unique_id):
    try:
        room = Room.objects.get(unique_id=unique_id)
    except Room.DoesNotExist:
        return HttpResponse("방을 찾을 수 없습니다.", status=404)

    context = {
        'room': room,
        'share_link': request.build_absolute_uri(),
    }

    return render(request, 'room_detail.html', context)

logger = logging.getLogger(__name__) # 버그 로그 찍어보려구 한 것

def room_menu(request, unique_id):
    try:
        room = get_object_or_404(Room, unique_id=unique_id)

        # 추가된 부분: 새로운 방에 입장할 때마다 게스트 이름 초기화
        if 'current_room' not in request.session or request.session['current_room'] != unique_id:
            if 'guest_name' in request.session:
                del request.session['guest_name']
            request.session['current_room'] = unique_id
        
        # POST 요청 처리
        if request.method == 'POST':
            # 게스트 로그인 POST
            if 'guest_name' in request.POST:
                guest_name = request.POST.get('guest_name')
                password = request.POST.get('password')
                request.session['guest_name'] = guest_name
                request.session['password'] = password
                return JsonResponse({'success': True})
            
            # 메뉴 선택 POST
            elif 'menus' in request.POST:
                guest_name = request.session.get('guest_name')
                password = request.session.get('password')
                if not guest_name:
                    return JsonResponse({'error': 'Guest name not found'}, status=400)
                
                menus = json.loads(request.POST.get('menus'))
                
                if not menus:
                    return JsonResponse({'error': 'No menus selected'}, status=400)
                
                GuestOrder.objects.create(
                    room=room,
                    guest_name=guest_name,
                    password=password,
                    menus=json.dumps(menus)
                )
                
                return JsonResponse({'success': True, 'redirect_url': reverse('room_orders', args=[unique_id])})
        
        # GET 요청 처리
        guest_name = request.session.get('guest_name')
        menus = []
        if guest_name:
            try:
                cafe = Cafe.objects.get(name=room.cafe)
                menus = MenuItem.objects.filter(cafe=cafe).values('id', 'name', 'image_url')
            except Cafe.DoesNotExist:
                logger.error(f"Cafe not found: {room.cafe}")
        
        context = {
            'room': room,
            'guest_name': guest_name,
            'menus': menus,
        }
        return render(request, 'room_menu.html', context)

    except Exception as e:
        logger.error(f"Unexpected error in room_menu view: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

def room_orders(request, unique_id): 
    try:
        room = get_object_or_404(Room, unique_id=unique_id)
        
        # 주문 초기화 POST
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            guest_name = request.session.get('guest_name')
            password = request.session.get('password')
            if guest_name:
                GuestOrder.objects.filter(room=room, guest_name=guest_name, password=password).delete()
                if 'guest_name' in request.session:
                    # del request.session['guest_name']
                    return JsonResponse({'success': True, 'message': '주문이 초기화되었습니다.'})
            return JsonResponse({'success': False, 'message': '사용자를 찾을 수 없습니다.'})

        guest_orders = GuestOrder.objects.filter(room=room)
        
        orders_details = []
        for order in guest_orders:
            menus = json.loads(order.menus)
            order_menus = []
            for menu in menus:
                menu_id = menu['id']
                options = menu['options']
                menu_item = MenuItem.objects.get(id=menu_id)
                order_menus.append({
                    'name': menu_item.name,
                    'options': options
                })
            orders_details.append({
                'guest_name': order.guest_name,
                'menus': order_menus,
            })
        
        context = {
            'room': room,
            'orders_details': orders_details,
        }
        return render(request, 'room_orders.html', context)

    except Exception as e:
        logger.error(f"Unexpected error in room_orders view: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)