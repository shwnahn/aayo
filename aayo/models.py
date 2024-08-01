# models.py
from django.db import models

# 방 정보를 저장하는 모델
class Room(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)
    cafe = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.cafe}"

# 게스트 주문 정보를 저장하는 모델
class GuestOrder(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=50)
    menus = models.TextField()  # JSON 문자열을 저장할 TextField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name}'s order in {self.room.name}"