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

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    return render(request, "home.html")

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
