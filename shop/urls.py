from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('contact/', views.contact, name='contact'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]