from django.contrib import admin
from .models import *

# Register your models here.ss
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room','image']

admin.site.register(Employee)
admin.site.register(Rooms)
admin.site.register(RoomImage, RoomImageAdmin)