from django.shortcuts import render, get_object_or_404
from .models import Service, Doctor

# lab 5: крок 1 - додано модель Service; крок 2 - products view бере послуги з БД; крок 3 - шаблон products їх відображає
# lab 6: крок 1 - додано view service_detail для детальної сторінки послуги з можливістю вибору лікаря, а також doctors view для фільтрації рейтингів
# lab 6: крок 9 - додано показ топ 3 лікаря на головній сторінці

def services(request):
    all_services = Service.objects.all()
    context = {
        'title': 'Наші послуги',
        'services': all_services,
    }
    return render(request, 'shop/services.html', context)

def home(request):
    # lab 6: крок 9 - на головній сторінці показати топ 3 лікаря замість статичного списку послуг
    doctors = Doctor.objects.all()[:3]
    context = {
        'title': 'Crunch',
        'message': 'Main page',
        'doctors': doctors
    }
    return render(request, 'shop/home.html', context)

def about(request):
    context = {
        'title': 'About shop',
        'description': 'Welcome!'
    }
    return render(request, 'shop/about.html', context)

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    # lab 6: крок 9 - додано фільтрацію лікарів за процедурами для відображення тільки тих, хто проводить цю послугу
    doctors = Doctor.objects.filter(procedures=service)
    context = {
        'title': service.name,
        'service': service,
        'doctors': doctors
    }
    return render(request, 'shop/service_detail.html', context)

def contact(request):
    context = {
        'title': 'Our',
        'email': 'shoping@example.com',
        'phone': '+380 34 234 4234'
    }
    return render(request, 'shop/contact.html', context)

def doctors(request):
    # Оновлено: фільтрація лікарів за послугами (процедурами)
    service_filter = request.GET.get('service')
    doctors = Doctor.objects.all()
    if service_filter:
        try:
            service_id = int(service_filter)
            doctors = doctors.filter(procedures__id=service_id)
        except ValueError:
            pass  # ignore invalid service
    
    # Отримуємо всі послуги для фільтра
    all_services = Service.objects.all()
    
    context = {
        'title': 'Наші лікарі',
        'doctors': doctors,
        'services': all_services,
        'current_service': service_filter
    }
    return render(request, 'shop/doctors.html', context)

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    context = {
        'title': doctor.name,
        'doctor': doctor
    }
    return render(request, 'shop/doctor_detail.html', context)