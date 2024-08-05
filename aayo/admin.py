# admin.py
from django.contrib import admin
from .models import *

admin.register(Room)
admin.site.register(GuestOrder)

class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_eng')
    search_fields = ('name', 'name_eng')
    
    # 상세보기 설정
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('menu_items')

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'image_url')
    list_filter = ('cafe',)
    search_fields = ('name', 'cafe__name')

# Register your models here
admin.site.register(Cafe, CafeAdmin)
admin.site.register(MenuItem, MenuItemAdmin)