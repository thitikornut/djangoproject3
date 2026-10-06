from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Service, DogBooking
from .forms import CustomerRegisterForm

# --- 1. หน้าทั่วไป ---

def home(request):
    """หน้าแรกของเว็บไซต์"""
    services_preview = Service.objects.filter(is_active=True)[:3]  # ดึงบริการมาแสดงตัวอย่าง 3 รายการ
    return render(request, 'myapp/home.html', {'services_preview': services_preview})

def about(request):
    """หน้าเกี่ยวกับเรา"""
    return render(request, 'myapp/about.html')

def contact(request):
    """หน้าติดต่อเรา"""
    return render(request, 'myapp/contact.html')


# --- 2. หน้าบริการและการจองคิว ---

def services(request):
    """หน้าบริการทั้งหมด และแบบฟอร์มจองคิวนำหมาเข้ารับบริการ"""
    if request.method == 'POST':
        # เช็กว่าผู้ใช้งานเข้าสู่ระบบหรือยัง
        if not request.user.is_authenticated:
            messages.error(request, 'กรุณาเข้าสู่ระบบก่อนทำการจองคิวเข้ารับบริการ')
            return redirect('login')

        # รับข้อมูลจากแบบฟอร์ม
        dog_name = request.POST.get('dog_name')
        breed = request.POST.get('breed')
        service_id = request.POST.get('service')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        note = request.POST.get('note', '')

        # ค้นหาวัตถุบริการจาก ID
        service_obj = get_object_or_404(Service, id=service_id)

        # บันทึกข้อมูลการจองลงในฐานข้อมูล
        DogBooking.objects.create(
            user=request.user,
            dog_name=dog_name,
            breed=breed,
            service=service_obj,
            booking_date=booking_date,
            booking_time=booking_time,
            note=note
        )

        # แจ้งเตือนยืนยันความสำเร็จ
        messages.success(
            request, 
            f'🎉 จองคิวสำเร็จแล้ว! สำหรับน้อง "{dog_name}" ในวันที่ {booking_date} เวลา {booking_time} น.'
        )
        return redirect('services')

    # ดึงบริการเฉพาะที่เปิดใช้งานอยู่
    service_list = Service.objects.filter(is_active=True)
    return render(request, 'myapp/services.html', {'services': service_list})


# --- 3. ระบบยืนยันตัวตน (Authentication) ---

def register(request):
    """หน้าลงทะเบียนสมาชิกใหม่"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # สมัครเสร็จแล้วให้เข้าสู่ระบบทันที
            messages.success(request, f'สมัครสมาชิกสำเร็จ! ยินดีต้อนรับคุณ {user.username}')
            return redirect('profile')
        else:
            messages.error(request, 'เกิดข้อผิดพลาด กรุณาตรวจสอบข้อมูลที่กรอกอีกครั้ง')
    else:
        form = CustomerRegisterForm()

    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    """หน้าเข้าสู่ระบบ"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ยินดีต้อนรับกลับมา คุณ {username}!')
                return redirect('profile')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})


def logout_view(request):
    """ออกจากระบบ"""
    logout(request)
    messages.info(request, 'ออกจากระบบเรียบร้อยแล้ว')
    return redirect('home')


# --- 4. หน้าโปรไฟล์ส่วนตัว ---

@login_required(login_url='login')
def profile(request):
    """หน้าโปรไฟล์ผู้ใช้งาน และแสดงประวัติการจองคิว"""
    # ดึงรายการจองคิวเฉพาะของผู้ใช้งานคนนี้ เรียงตามวันที่ล่าสุด
    user_bookings = DogBooking.objects.filter(user=request.user).order_by('-created_at') if hasattr(DogBooking, 'user') else []
    
    context = {
        'user': request.user,
        'bookings': user_bookings,
    }
    return render(request, 'myapp/profile.html', context)