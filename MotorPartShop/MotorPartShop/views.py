from django.shortcuts import render
from parts.models import Part, Category

def home(request):
    featured_parts = Part.objects.filter(stock__gt=0)[:4]
    return render(request, 'home.html', {'featured_parts': featured_parts})

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

