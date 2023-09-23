from django.contrib import admin
from .models import *

# Register your models here.ss
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room','image']

class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_first_name', 'client_email']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['client', 'street', 'city', 'state']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['client', 'room', 'check_in', 'check_out', 'reservation_number']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'username', 'email']
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'room_type', 'price_per_night']

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Rooms, RoomAdmin)
admin.site.register(RoomImage, RoomImageAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Address, AddressAdmin)