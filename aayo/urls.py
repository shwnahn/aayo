from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('room/', views.room, name='room'),
    # 메인, 방 생성 form (main -> room 이름 변경)

    path('room/<str:unique_id>/', views.room_detail, name='room_detail'), 
    # 방 개요 (방 이름, 방 링크 정보 보여주기) (리디렉션(버튼) : 방 입장 / 링크 공유 / 주문 총계)

    path('room/<str:unique_id>/menu/', views.room_menu, name='room_menu'),
    # 방 입장 후 주문, 선택된 카페 보여주기 (로그인(이름 작성), 메뉴(크롤링) 선택 → 상세 선택(모달))

    path('room/<str:unique_id>/orders/', views.room_orders, name='room_orders'),
    # 주문 총계 / 메뉴 커스텀 정보 보기

    path('ads.txt/', views.ads, name='ads'),
]