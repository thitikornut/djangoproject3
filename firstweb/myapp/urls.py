from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),    # เพิ่มบรรทัดนี้
    path('logout/', views.logout_view, name='logout'),  # เพิ่มบรรทัดนี้
]