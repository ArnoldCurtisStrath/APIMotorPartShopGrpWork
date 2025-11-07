from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def parts(request):
    parts_list = [
        {'name': 'Engine Oil Filter', 'price': 1599},
        {'name': 'Brake Pads', 'price': 4550},
        {'name': 'Air Filter', 'price': 1275},
        {'name': 'Spark Plugs', 'price': 899},
    ]
    return render(request, 'parts.html', {'parts': parts_list})
