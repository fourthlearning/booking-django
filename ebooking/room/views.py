#import json
from builtins import object
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from room.models import Booking, Room

#from datetime import datetime
# Create your views here.
"""
-------Login & Logout & Register---------
"""
def my_login(request):
    context = {}

    if request.method == 'POST': #รับค่า POST จาก from
        username = request.POST.get('username') # รับ user
        password = request.POST.get('password') # รับ password

        user = authenticate(request, username=username, password=password) # เปรียนเทียบuesrname password

        if user: 
            login(request, user) 

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='login.html', context=context)


@login_required
def my_logout(request):
    logout(request)
    return redirect('login') #พอกด logout ก้จะไปหน้า login


def my_register(request):
    context = dict()
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email')
        )
        group = Group.objects.get(name='user') #คนที่สมัครในส่วนนี้ก้อยู่ในกลุ่ม User ทั้งหมด
        user.groups.add(group) #ตััว User ข้างบน จะถูก add
        user.save() #save
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) # เปรียนเทียบuesrname password

        if user:
            login(request, user)

            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    
    return render(request, template_name='register.html', context=context)





"""
---------------หน้าหลัก-------------
"""
@login_required
def index(request):
    """
        Index page - หน้าจอรายการห้องทั้งหมด
    """
    room = Room.objects.all()
    context ={}
    if request.method == 'POST':
        search = request.POST.get('search')
        search_txt = Room.objects.filter(
            name__icontains = search
        )
        return render(request, 'room/index.html', context={
        'room': search_txt
         })
    return render(request, 'room/index.html', context={
        'room': room
    })






"""
-----------------เพิ่มคำร้อง-----------------
"""
@login_required
@permission_required('room.add_booking')
def booking(request):
    search = request.GET.get('search', '')
    room = Room.objects.all()
    booklist = Booking.objects.all() 
    #user = Booking.objects.get(pk=user_name)
    

    if request.method == 'POST':
        book_date_raw = request.POST.get('book_date').split('/')[::-1]
        book_date_raw[1], book_date_raw[2] = book_date_raw[2], book_date_raw[1]
        # print('-'.join(book_date_raw))
        book_date_raw = '-'.join(book_date_raw)
        # print("Room is" ,request.POST.get('room_name'))
        booking = Booking(
            book_date = book_date_raw,
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            description =request.POST.get('description'),
            book_by = User.objects.get(username=request.user),
            room_id = Room.objects.get(pk=request.POST.get('room_name'))
        )
        booking.save()
        
    else:
        booking = Booking.objects.none()

    context = {
        'room' : room,
        'booking': booking
        
    }

    
    return render(request, template_name='room/book_list.html', context=context)


"""
--------------รายละเอียดการจอง---------------------
"""

@login_required
@permission_required('room.view_booking')
def requestlist(request):
    booking = Booking.objects.all()
    context ={}

    
    return render(request, template_name='room/requestlist.html', context={
        'booking': booking
    })





"""
--------------เพิ่มห้อง อัพเดตและแก้ไขห้อง----------------------
"""
@login_required
@permission_required('room.add_room')
def room_add(request):
    """
        เพิ่มข้อมูล room ใหม่เข้าสู่ฐานข้อมูล
    """
    #ดึงข้อมูลในระบบออกมา
    rooms = Room.objects.all() 
    msg = ''

    if request.method == 'POST':
        room = Room.objects.create(
            name = request.POST.get('name'),
            open_time=request.POST.get('open_time'),
            close_time=request.POST.get('close_time'),
            capacity =request.POST.get('capacity')
        )
        room.save()
        msg = 'Successfully create new room - name : %s' % (room.name)
    else:
        room = Room.objects.none()

    context = {
        'room' : room,
        'msg': msg
    }

    return render(request, 'room/room_add.html', context=context)



@login_required 
@permission_required('room.change_room')
def room_update(request, room_id):
    """
        #Update ข้อมูลห้องที่มี id = room_id
    """
    
    try:
        room = Room.objects.get(pk=room_id)
        booking = Booking.objects.all()
        
        msg = ''
    except Room.DoesNotExist: #ถ้าส่งidบะหาไม่เจอ ให้rediect to room_list
        return redirect('index')

    if request.method == 'POST':
        room.room_id=request.POST.get('room_id')
        room.name=request.POST.get('name')
        room.open_time=request.POST.get('open_time')
        room.close_time=request.POST.get('close_time')
        room.capacity=request.POST.get('capacity')

        room.save()
        msg = 'Successfully update room : %s' % (room.name)
    
    context = {
        'room': room,    
        'msg': msg
    }

    return render(request, 'room/room_add.html', context=context)




    """"
    ลบห้อง
    """
@login_required
@permission_required('room.delete_room')
def room_delete(request, room_id):
    """
        #ลบข้อมูล classroom โดยลบข้อมูลที่มี id = class_id
    """
    room = Room.objects.get(id = room_id)
    room.delete()
    return redirect(to='index')






"""
----------------หน้าอนุมัติ-------------------
"""
@login_required
@permission_required('room.change_booking')
def requestlist_edit(request, request_id):
    """
        ดึงข้อมูลจาก requestlist
    """
    if request.method == 'POST':
        if request.POST.get('checkbox') == 'comfirm':
            status = True
        else:
            status = False
        remark = request.POST.get('statusremark')

        booking = Booking.objects.get(pk=request_id)
        booking.status = status
        booking.status_remark = remark
        booking.save()
        booking = Booking.objects.all()

    
        return render(request, template_name='room/requestlist.html', context={
        'booking': booking
        })
    room_id = Booking.objects.get(pk=request_id)
    context = {
        'bk' : room_id
    }
    return render(request, 'room/request_edit.html', context=context)
