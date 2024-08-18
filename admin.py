# admin.py
from django.contrib import admin
from .models import *

admin.register(Room)
admin.site.register(GuestOrder)
admin.site.register(Cafe)
admin.site.register(MenuItem)