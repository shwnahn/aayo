from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('room/<str:unique_id>/', views.room_detail, name='room_detail'),
    path('room/<str:unique_id>/share/', views.share_link, name='share_link'),
    path('room/<str:unique_id>/menu/', views.room_menu, name='room_menu'),
    path('room/<str:unique_id>/orders/', views.room_orders, name='room_orders'),
]