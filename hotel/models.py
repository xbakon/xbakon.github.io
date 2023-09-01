from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

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
        return self.room_name

class RoomImage(models.Model):
    room = models.ForeignKey(Rooms, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()