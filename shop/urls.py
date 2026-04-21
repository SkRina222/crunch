from django.urls import path
from . import views

app_name = 'shop'

# lab 6: крок 1 - додано URL для service_detail
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('contact/', views.contact, name='contact'),
]