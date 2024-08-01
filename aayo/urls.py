# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'), # 호스트가 방을 생성하는 폼이 있는 화면
    path('room/<str:unique_id>/', views.room_detail, name='room_detail'), # 호스트가 방을 생성하고 공유하기 전 확인하는 화면
    path('join/<str:unique_id>/', views.room_view, name='room_view'), # 게스트가 초대된 방의 상세 정보를 확인하고 입장할 수 있는 화면
    path('enter-room/<str:unique_id>/', views.enter_room, name='enter_room'), # 방에 들어가기 전에 
    path('room/<str:unique_id>/menu/', views.room_menu, name='room_menu'), # 카페 메뉴를 크롤링해서 게스트에게 보여주는 화면
    path('room/<str:unique_id>/confirm/', views.confirm_menu, name='confirm_menu'),
    path('room/<str:unique_id>/order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/total/', views.order_total, name='order_total'),
    path('room/<str:unique_id>/order_total/', views.order_total, name='order_total'),
    path('room/<str:unique_id>/reset_order/', views.reset_order, name='reset_order'), # 게스트가 다시 고르기를 눌렀을 때 기존 주문 정보 삭제
]