from django.contrib import admin
from .models import Service, DogBooking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(DogBooking)
class DogBookingAdmin(admin.ModelAdmin):
    # แสดงคอลัมน์ที่ตรงกับ field ใน models.py ใหม่
    list_display = ('id', 'user', 'dog_name', 'breed', 'service', 'booking_date', 'booking_time', 'created_at')
    list_filter = ('booking_date', 'service')
    search_fields = ('dog_name', 'breed', 'user__username', 'note')