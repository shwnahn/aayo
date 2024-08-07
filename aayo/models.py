# models.py
from django.db import models

# 방 정보를 저장하는 모델
class Room(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=50, blank=True, null=True)
    cafe = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=8, unique=True)
    def __str__(self):
        return f"{self.name}"
    
# 카페 / 메뉴
class Cafe(models.Model):
    name = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=450, blank=True, null=True)  # 이미지 URL 필드 추가
    category = models.CharField(max_length=50, blank=True, null=True) # 카테고리 추가
    note = models.TextField(blank=True, null=True) #비고란 추가
    def __str__(self):
        return f"{self.name} ({self.cafe.name})"

# 게스트 주문 정보를 저장하는 모델
class GuestOrder(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)
    menus = models.TextField()  # JSON 문자열을 저장할 TextField
    def __str__(self):
        return f"{self.guest_name}의 주문"