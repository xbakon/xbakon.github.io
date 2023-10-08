from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q

# Create your models here.

class Employee(AbstractUser):
    SUPERVISOR = 'Supervisor'
    EMPLOYEE = 'Employee'
    FRONT_DESK = 'Front Desk'
    MAINTAINENCE = 'Maintainence'
    HOUSEKEEPING = 'Housekeeping'
    username = models.CharField(max_length=8, unique=True)
    middle_name = models.CharField(max_length=100)
    type_of_employee = models.CharField(max_length=50, choices=[(SUPERVISOR, 'Supervisor'),(EMPLOYEE, 'Employee')])
    addrress = models.CharField(max_length=250)
    position = models.CharField(max_length=50, choices=[(FRONT_DESK, 'Front Desk'),(MAINTAINENCE, 'Maintainence'),(HOUSEKEEPING, 'Housekeeping')])
    ssn = models.IntegerField(
        validators=[
            MaxValueValidator(99999999),
            MinValueValidator(10000000)
        ], blank=True, null=True
    )
    supervisor_code = models.IntegerField(
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(1000)
        ], unique=True, blank=True, null=True
    )
    phno = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self) -> str:
        return self.first_name


class Rooms(models.Model):
    FLOOR1 = '1st Floor'
    FLOOR2 = '2nd Floor'
    FLOOR3 = '3rd Floor'
    ROYAL = 'THE ROYAL'
    GRAND = 'THE GRAND'
    LUXURY = 'LUXURY SUITE'
    room_title = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100, choices=[(ROYAL, 'THE ROYAL'), (GRAND, 'THE GRAND'), (LUXURY, 'LUXURY SUITE')])
    room_name = models.CharField(max_length=100)
    room_floor = models.CharField(max_length=50, choices=[(FLOOR1, '1st Floor'),(FLOOR2, '2nd Floor'),(FLOOR3, '3rd Floor')])
    room_description = models.CharField(max_length=300)
    price_per_night = models.IntegerField()

    def __str__(self) -> str:
        room_str = self.room_name + " (" + self.room_type + ")"
        return room_str

class RoomImage(models.Model):
    room = models.ForeignKey(Rooms, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()

class Client(models.Model):
    client_first_name = models.CharField(max_length=100)
    client_last_name = models.CharField(max_length=100)
    client_dob = models.DateField()
    client_phno = models.IntegerField()
    client_email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.client_email

class Reservation(models.Model):
    reservation_number = models.PositiveIntegerField(unique=True)
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    room = models.ForeignKey(Rooms, related_name='reservation', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='client_reservation', on_delete=models.CASCADE)
    no_of_childrens = models.IntegerField(choices=[(ZERO, 0), (ONE, 1), (TWO, 2)])
    no_of_adults = models.IntegerField(choices=[(ONE, 1), (TWO, 2), (THREE, 3)])
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self) -> str:
        return self.room.room_name

    def get_display_price(self):
        return "{0:.2f}".format(self.room.price_per_night / 100)

class Address(models.Model):
    client = models.ForeignKey(Client, related_name='address', on_delete=models.CASCADE)
    street = models.CharField(max_length=150)
    apt = models.IntegerField(null=True,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()

    def __str__(self) -> str:
        return self.client.client_email
