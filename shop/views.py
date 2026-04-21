from django.shortcuts import render, get_object_or_404
from .models import Service

# lab 5: крок 1 - додано модель Service; крок 2 - products view бере послуги з БД; крок 3 - шаблон products їх відображає
# lab 6: крок 1 - додано view service_detail для детальної сторінки послуги

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

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    context = {
        'title': service.name,
        'service': service
    }
    return render(request, 'shop/service_detail.html', context)

def contact(request):
    context = {
        'title': 'Our',
        'email': 'shoping@example.com',
        'phone': '+380 34 234 4234'
    }
    return render(request, 'shop/contact.html', context)