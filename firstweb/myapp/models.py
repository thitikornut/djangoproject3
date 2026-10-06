from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="ชื่อบริการ")
    description = models.TextField(verbose_name="รายละเอียดบริการ")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา (บาท)")
    icon_class = models.CharField(
        max_length=50, 
        default="fa-solid fa-dog", 
        help_text="ชื่อคลาส FontAwesome เช่น fa-solid fa-dog, fa-solid fa-bath",
        verbose_name="ไอคอน"
    )
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DogBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้จอง")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="บริการ")
    dog_name = models.CharField(max_length=100, verbose_name="ชื่อสุนัข")
    breed = models.CharField(max_length=100, verbose_name="สายพันธุ์")
    booking_date = models.DateField(verbose_name="วันที่เข้ารับบริการ")
    booking_time = models.TimeField(verbose_name="เวลาที่สะดวก")
    note = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dog_name} - {self.service.title} ({self.booking_date})"