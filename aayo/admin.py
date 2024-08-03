# admin.py
from django.contrib import admin
from .models import *

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'cafe', 'unique_id', 'created_at')
    list_filter = ('cafe', 'created_at')
    search_fields = ('name', 'unique_id')
    readonly_fields = ('unique_id', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'cafe', 'password')
        }),
        ('추가 정보', {
            'fields': ('unique_id', 'created_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(GuestOrder)
admin.site.register(Cafe)
admin.site.register(MenuItem)