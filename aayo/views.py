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
import logging

def generate_unique_id(): # 방 뒤에 생성되는 유니크 url을 생성하는 함수이다.
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def index(request): # 메인 화면 렌더링 함수
    return render(request, 'index.html')

def room(request): # 방 생성 함수 
    # POST 요청 처리 (방 생성하기)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password') # 숨기기 처리 해놓음
        cafe_name = request.POST.get('cafe')
        print(cafe_name)
        cafe = Cafe.objects.get(name=cafe_name)
        print(cafe)
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
    
    # GET 요청 처리
    ctx = {
        'cafes': Cafe.objects.all(),
    }
    return render(request, 'room.html', ctx)

def room_detail(request, unique_id):
    try:
        room = Room.objects.get(unique_id=unique_id)
        cafe = Cafe.objects.get(name=room.cafe)
    except Room.DoesNotExist:
        return HttpResponse("방을 찾을 수 없습니다.", status=404)

    context = {
        'cafe': cafe,
        'room': room,
        'share_link': request.build_absolute_uri(),
    }

    return render(request, 'room_detail.html', context)

logger = logging.getLogger(__name__) # 버그 로그 찍어보려구 한 것

def room_menu(request, unique_id):
    room = get_object_or_404(Room, unique_id=unique_id)
    cafe = Cafe.objects.get(name=room.cafe) # name_eng 가져오기 위해 추가

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
        elif 'menu_details' in request.POST:
            guest_name = request.session.get('guest_name')
            password = request.session.get('password')
            if not guest_name:
                return JsonResponse({'error': 'Guest name not found'}, status=400)
            
            menu_details = json.loads(request.POST.get('menu_details'))
            if not menu_details:
                return JsonResponse({'error': 'No menu_details selected'}, status=400)
            
            # 기존 GuestOrder 업데이트 또는 생성
            guest_order, created = GuestOrder.objects.update_or_create(
                room=room,
                guest_name=guest_name,
                password=password,
                defaults={}
                # menus 필드 삭제
            )
            
            # 기존 OrderItem 삭제 후 새로 추가
            guest_order.order_items.all().delete()
            
            # OrderItems 새로 추가 - Sihwan
            for menu in menu_details:
                try:
                    menu_item = MenuItem.objects.get(id=menu['id'])
                    OrderItem.objects.create(
                        order=guest_order,
                        menu_item=menu_item,
                        temperature=menu['options']['temperature'],
                        size=menu['options']['size'],
                        ice=menu['options']['ice'],
                        note=menu['options']['note'],
                    )
                except MenuItem.DoesNotExist:
                    return JsonResponse({'error': f'MenuItem with id {menu["id"]} not found'}, status=400)

            return JsonResponse({'success': True, 'redirect_url': reverse('room_orders', args=[unique_id])})
    
    # GET 요청 처리
    if request.method == 'GET':
        guest_name = request.session.get('guest_name')
        password = request.session.get('password')
        menu_items = MenuItem.objects.filter(cafe=cafe)
        selected_menu_ids = []
        selected_menu_options = {}

        if guest_name:
            try:
                guest_order = GuestOrder.objects.filter(guest_name=guest_name, password=password, room=room).first()
                if guest_order:
                    order_items = OrderItem.objects.filter(order=guest_order)
                    selected_menu_ids = [item.menu_item.id for item in order_items]
                    for item in order_items:
                        selected_menu_options[item.menu_item.id] = {
                            'temperature': item.temperature,
                            'size': item.size,
                            'ice': item.ice,
                            'note': item.note
                        }
                    
                    print('Selected Menu IDs:', selected_menu_ids) 
            except Cafe.DoesNotExist:
                logger.error(f"Cafe not found: {room.cafe}")
        
       
        context = {
            'room': room,
            'guest_name': guest_name,
            'menu_items': menu_items,
            'selected_menu_ids': selected_menu_ids,
            'selected_menu_options': selected_menu_options,
            'cafe': cafe # 이 줄 추가 (로고 가져오기)
        }
        return render(request, 'room_menu.html', context)

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

       # 모든 OrderItem 가져오기
        order_items = OrderItem.objects.filter(order__room=room)
        
        orders_details = []
        for item in order_items:
            orders_details.append({
                'guest_name': item.order.guest_name,
                'menu_item': {
                    'name': item.menu_item.name,
                    'image_url': item.menu_item.image_url
                },
                'options': {
                    'temperature': item.temperature,
                    'size': item.size,
                    'ice': item.ice,
                    'note': item.note
                }
            })
        
        context = {
            'room': room,
            'orders_details': orders_details,
        }
        return render(request, 'room_orders.html', context)

    except Exception as e:
        logger.error(f"Unexpected error in room_orders view: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred'}, status=500)

def ads(request):
    return render(request, 'ads.txt', content_type='text/plain')