from django.urls import path
from . import views

urlpatterns = [
    path('', , name='main'), 
    # 메인, 방 생성 form

    path('room/<str:unique_id>/', , name='room_detail'), 
    # 방 개요 (방 이름, 방 링크 정보 보여주기) (리디렉션(버튼) : 방 입장 / 링크 공유 / 주문 총계)

    path('room/<str:unique_id>/menu/', , name='room_menu'),
    # 방 입장 후 주문, 선택된 카페 보여주기 (로그인(이름 작성), 메뉴(크롤링) 선택 → 상세 선택(모달))

    path('room/<str:unique_id>/orders/', , name='room_orders'),
    # 주문 총계 / 메뉴 커스텀 정보 보기
]