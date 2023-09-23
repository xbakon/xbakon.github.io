from django.shortcuts import render, redirect
from .models import *
import secrets
import string
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .utils import send_email
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
from datetime import datetime
import re
from dateutil import parser
from datetime import timedelta
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    if request.GET.get('end_date'):
        start_date = request.GET.get('end_date')
        start_date = datetime.strptime(start_date, "%d-%m-%y")
        start_date = start_date + timedelta(days=1)
        page_number = int(request.GET.get('page_number'))
        page_number = page_number + 1
    elif request.GET.get('start_date'):
        start_date = request.GET.get('start_date')
        start_date = datetime.strptime(start_date, "%d-%m-%y")
        start_date = start_date - timedelta(days=5)
        page_number = int(request.GET.get('page_number'))
        page_number = page_number - 1
    else:
        start_date = timezone.now().date()
        page_number = 1

    selected_room_type = request.GET.get('room_type', 'THE ROYAL')
    end_date = start_date + timedelta(days=5)
    rooms = Rooms.objects.filter(room_type=selected_room_type)

    reservations = Reservation.objects.filter(
        room__room_type=selected_room_type,
        check_in__gte=start_date,
        check_in__lte=end_date,
    ).order_by('room__room_name', 'check_in')

    if reservations.exists():
        for reservation in reservations:
            print("Room Name: ", reservation.room.room_name)
            print("Check In: ", reservation.check_in)
            print("Check Out: ", reservation.check_out)
            print("-----------------------------")
    print(selected_room_type)

    room_types = Rooms.objects.values_list('room_type', flat=True).distinct()
    dates = []
    str_dates = []
    for i in range(5):
        date = start_date + timedelta(days=i)
        str_date = date.strftime("%d-%m-%y")
        str_date = str(str_date)
        str_dates.append(str_date)
        date = date.strftime("%Y-%m-%d")
        date = datetime.strptime(date, "%Y-%m-%d").date()
        dates.append(date)
        
    context = {
        'selected_room_type': selected_room_type,
        'room_types': room_types,
        'reservations': reservations,
        'start_date': start_date,
        'end_date': end_date,
        'rooms': rooms,
        'dates': dates,
        'str_dates': str_dates,
        'my_end_date': str_dates[-1],
        'my_start_date': str_dates[0],
        'page_number': page_number
    }

    return render(request, 'home.html', context)

def login_page(request):
    if request.method == 'POST':
        current_employee = request.POST

        if not Employee.objects.filter(username= current_employee['username']).exists():
            messages.info(request, "Invalid username!")
            return redirect("/login/")
        employee = Employee.objects.filter(username=current_employee['username'])
        employee = employee[0]
        password_match = check_password(current_employee['password'], employee.password)

        if password_match:
            print("Password is correct")
            login(request, employee)
            authenticated_user = employee
            return redirect('/')

        else:
            messages.info(request, "Invalid password!")
            return redirect("/login/")

    return render(request, "login.html")

def new_employee(request):
    if request.method == 'POST':
        data = request.POST

        if data['password'] != data['re_password']:
            messages.info(request, "password and confirm password should be identical!")
            return redirect("/new-employee/")
        same_email = Employee.objects.filter(email=data['email'])

        if same_email.exists():
            messages.info(request, "Email already in use!")
            return redirect("/new-employee/")


        characters = string.ascii_letters + string.digits
        username = ''.join(secrets.choice(characters) for _ in range(8))

        type_of_employee = data['type']
        print(type_of_employee)
        ssn = data['ssn']
        supervisor_code = 0
        print(data['position'])

        if type_of_employee == "Supervisor":
            supervisor_code = ssn[-4:]
            print(supervisor_code)

        employee = Employee(first_name=data['first_name'], middle_name=data['middle_name'], 
        last_name=data['last_name'], type_of_employee=data['type'], addrress=data['address'],
        ssn=data['ssn'], supervisor_code=supervisor_code, phno=data['phno'], email=data['email'],
        username=username, position=data['position']
        )
        employee.set_password(data['password'])
        employee.save()
        return render(request, "login.html", {'username': username})

    return render(request, "new-employee.html")


def logout_user(request):
    logout(request)
    return redirect('/login/')

def forgot_password(request):
    # if request.method == 'POST':
    #     print("Email is: ", authenticated_user['email'])
    return render(request, "forgot_password.html")

def generate_otp(request):
    if request.method == 'POST':
        data = request.POST
        print(data['username'])
        employee = Employee.objects.filter(username=data['username'])
        flag = 0

        if not employee.exists():
            print("*Invalid username!")
        else:
            print("*OTP sent to your email!")
            flag = 1

            employee = employee[0]
            code = send_email(employee.email)
            print(code)
        
        data = {
            'flag': flag,
            'otp': code
        }

        return JsonResponse(data)
    return render(request, "forgot_password.html")

def change_password(request):
    if request.method == 'POST':
        data = request.POST
        print(data['username'])

        employee = Employee.objects.filter(username=data['username'])

        if not employee.exists():
            print("*Invalid username!")
            return render(request, "forgot_password.html", {'text': '*Invalid username!'})
        else:
            employee = employee[0]
            if data['hidden_otp'] != data['otp']:
                return render(request, "forgot_password.html", {'text': '*Invalid OTP!'})
            
            if data['password'] != data['re_password']:
                return render(request, "forgot_password.html", {'text': '*password and confirm password should be identical!'})

            
            employee = Employee.objects.filter(username=data['username'])
            employee = employee[0]
            employee.set_password(data['password'])
            employee.save()
            return render(request, "login.html")

    return redirect('/forgot-password/')

def rooms(request):
    my_rooms = Rooms.objects.all()
    room_images_dict = {}
    for room in my_rooms:
        room_images = RoomImage.objects.filter(room=room)
        room_images_dict[room.id] = room_images

    return render(request, "rooms.html", {'rooms': my_rooms, 'room_images_dict': room_images_dict})

def hotel_room(request, roomId):
    room = Rooms.objects.get(id=roomId)
    images = RoomImage.objects.filter(room=room)
    return render(request, "hotel_room.html", {'roomId': roomId, 'room': room})

@login_required(login_url='/login/')
def reservation(request):
    if request.method == 'POST':
        data = request.POST
        selected_id = data['id']
    else:
        selected_id = None

    rooms = Rooms.objects.all()
    if not selected_id is None:
        selected_id = int(selected_id)

    return render(request, "reservation.html", {'selected_id': selected_id, 'rooms': rooms})

def get_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_name = data.get('room_name')
            room = Rooms.objects.filter(room_name=room_name)
            room = room[0]
            response_data = {
                'room_type': room.room_type,
                'room_floor': room.room_floor
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


def lookup_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            client_email = data.get('client_email')
            print(client_email)
            client = Client.objects.filter(client_email=client_email)

            if not client.exists():
                response_data = {
                    'error': '*email not found!'
                }
            else:
                client = client[0]
                address = Address.objects.filter(client=client)
                address = address[0]
                response_data = {
                    'first_name': client.client_first_name,
                    'last_name': client.client_last_name,
                    'dob': client.client_dob,
                    'phno': client.client_phno,
                    'street': address.street,
                    'apt': address.apt,
                    'city': address.city,
                    'state': address.state,
                    'zip_code': address.zip_code
                }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@login_required(login_url='/login/')
def make_resrvation(request):
    if request.method == 'POST':
        data = request.POST
        room_name = data['rooms']
        print(room_name)
        check_in = datetime.strptime(data['check_in'], '%Y-%m-%d').date()
        check_out = datetime.strptime(data['check_out'], '%Y-%m-%d').date()
        print(check_in)
        print(check_out)

        overlapping_reservations = Reservation.objects.filter(
            Q(check_in__lte=check_in, check_out__gte=check_in) |
            Q(check_in__lte=check_out, check_out__gte=check_out) |
            Q(check_in__gte=check_in, check_out__lte=check_out),
            room__room_name=room_name
        )

        if overlapping_reservations.exists():
            selected_id = None
            rooms = Rooms.objects.all()
            return render(request, "reservation.html", {'selected_id': selected_id, 'rooms': rooms, 'message': '*Reservation conflicts with existing reservations!', 'key': 0}) 
        else:
            email = data['email']
            client = Client.objects.filter(client_email=email)
            reservation_number = random.randint(10000000, 99999999)

            while Reservation.objects.filter(reservation_number=reservation_number).exists():
                reservation_number = random.randint(10000000, 99999999)

            if client.exists():
                reservation = Reservation.objects.create(
                    room=Rooms.objects.get(room_name=room_name),
                    client=client[0],
                    no_of_childrens=data['childs'],
                    no_of_adults=data['adults'],
                    check_in=check_in,
                    check_out=check_out,
                    reservation_number=reservation_number
                )
                reservation.save()
            else:
                dob = timezone.make_aware(timezone.datetime.strptime(data['dob'], "%Y-%m-%d"))
                client = Client.objects.create(
                    client_first_name=data['first_name'],
                    client_last_name=data['last_name'],
                    client_dob=dob,
                    client_phno=data['phno'],
                    client_email=email
                )
                client.save()

                if data['apt'] == "":
                    apt = None
                else:
                    apt = int(data['apt'])

                address = Address.objects.create(
                    client=client,
                    street=data['street'],
                    apt=apt,
                    city=data['city'],
                    state=data['state'],
                    zip_code=data['zip_code']
                )
                address.save()

                reservation = Reservation.objects.create(
                    room=Rooms.objects.get(room_name=room_name),
                    client=client,
                    no_of_childrens=data['childs'],
                    no_of_adults=data['adults'],
                    check_in=check_in_date,
                    check_out=check_out_date,
                    reservation_number=reservation_number
                )
                reservation.save()

            selected_id = None
            rooms = Rooms.objects.all()
            return render(request, "reservation.html", {'selected_id': selected_id, 'rooms': rooms, 'message': '*Reservation created successfuly!', 'key': 1, 'reservation_number': reservation_number})

    return redirect('/reservation/')

def search(request):
    if request.method == 'POST':
        data = request.POST
        reservation_number = data['reservation_number']

        if len(str(reservation_number)) < 8 or len(str(reservation_number)) > 8:
            return render(request, "search.html", {'message': 'reservation number must have exactly 8 digits'})
        reservation = Reservation.objects.filter(reservation_number=reservation_number)

        if not reservation.exists():
            return render(request, "search.html", {'message': 'reservation not found'})
        reservation = reservation[0]

        return redirect('/display-reservation/' + str(reservation.reservation_number))

    else:
        return render(request, "search.html")

@login_required(login_url='/login/')
def edit_reservation(request):
    if request.method == 'POST':
        data = request.POST
        reservation_number = data['reservation_number']

        if len(str(reservation_number)) < 8 or len(str(reservation_number)) > 8:
            return render(request, "search.html", {'message': 'reservation number must have exactly 8 digits'})
        reservation = Reservation.objects.filter(reservation_number=reservation_number)

        if not reservation.exists():
            return render(request, "search.html", {'message': 'reservation not found'})
        reservation = reservation[0]
        client = Client.objects.filter(id=reservation.client.id)
        room = Rooms.objects.filter(id=reservation.room.id)
        client = client[0]
        my_room = room[0]
        address = Address.objects.filter(client=client)
        address = address[0]
        rooms = Rooms.objects.all()

        return render(request, "edit_reservation.html", {'reservation': reservation, 'rooms': rooms, 'client': client, 'address': address, 'selected_id': my_room.id})

    return render(request, "edit.html")

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'POST':
        data = request.POST
        room_name = data['rooms']

        check_in = data['check_in']
        check_out = data['check_out']

        check_in = parser.parse(check_in)
        check_in = check_in.strftime("%Y-%m-%d")
        check_out = parser.parse(check_out)
        check_out = check_out.strftime("%Y-%m-%d")

        if check_out <= check_in:
            return render(request, "edit.html", {'message': 'check-out date cannot be less than or equal to check-in'})
        check_in_date = timezone.make_aware(timezone.datetime.strptime(check_in, "%Y-%m-%d"))
        check_out_date = timezone.make_aware(timezone.datetime.strptime(check_out, "%Y-%m-%d"))

        overlapping_reservations = Reservation.objects.filter(
            Q(check_in__lte=check_in, check_out__gte=check_in) |
            Q(check_in__lte=check_out, check_out__gte=check_out) |
            Q(check_in__gte=check_in, check_out__lte=check_out),
            room__room_name=room_name
        ).exclude(id=data['reservation_id'])

        if overlapping_reservations.exists():
            message = 'conflict in date for reservation number: ' + data['reservation_number']
            return render(request, "edit.html", {'message': message})

        reservation = Reservation.objects.filter(reservation_number=data['reservation_number'])
        reservation = reservation[0]
        reservation.check_in = check_in_date
        reservation.check_out = check_out_date
        reservation.no_of_adults = data['adults']
        reservation.no_of_childrens = data['childs']
        reservation.room = Rooms.objects.get(room_name=room_name)
        reservation.save()

        message = 'details updated for reservation number: ' + data['reservation_number']
        return render(request, "edit.html", {'message': message})

    return render(request, "edit.html")

def display_reservation(request, reservation_number):
    print(reservation_number)
    reservation = Reservation.objects.get(reservation_number=reservation_number)
    return render(request, "display_reservation.html", {'reservation': reservation})
