from django.shortcuts import render
from .models import Service

# lab 5: крок 1 - додано модель Service; крок 2 - products view бере послуги з БД; крок 3 - шаблон products їх відображає

def home(request):
    context = {
        'title': 'Crunch',
        'message': 'Main page'
    }
    return render(request, 'shop/home.html', context)

def about(request):
    context = {
        'title': 'About shop',
        'description': 'Welcome!'
    }
    return render(request, 'shop/about.html', context)

def products(request):
    services = Service.objects.all()
    context = {
        'title': 'Наші послуги',
        'services': services
    }
    return render(request, 'shop/products.html', context)

def contact(request):
    context = {
        'title': 'Our',
        'email': 'shoping@example.com',
        'phone': '+380 34 234 4234'
    }
    return render(request, 'shop/contact.html', context)