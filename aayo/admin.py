# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import *

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe')
admin.site.register(Room, RoomAdmin)

class GuestOrderAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name')
admin.site.register(GuestOrder, GuestOrderAdmin)

class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_eng')
    search_fields = ('name', 'name_eng')
    # 상세보기 설정
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('menu_items')
admin.site.register(Cafe, CafeAdmin)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'category', 'note', 'image_tag')
    list_filter = ('cafe',)
    search_fields = ('name', 'cafe__name')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image_url)
    image_tag.short_description = 'Image'
    
admin.site.register(MenuItem, MenuItemAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'temperature', 'size', 'ice', 'note')

admin.site.register(OrderItem, OrderItemAdmin)