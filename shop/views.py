from django.shortcuts import render

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
    context = {
        'title': 'Our product',
        'products': ['apple', 'cobblestone', 'Wood', 'Glass']
    }
    return render(request, 'shop/products.html', context)

def contact(request):
    context = {
        'title': 'Our',
        'email': 'shoping@example.com',
        'phone': '+380 34 234 4234'
    }
    return render(request, 'shop/contact.html', context)