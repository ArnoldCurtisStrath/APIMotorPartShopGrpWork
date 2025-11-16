from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Part, Category

def part_list(request):
    parts = Part.objects.all().select_related('category')
    paginator = Paginator(parts, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'parts/part_list.html', {'parts': page_obj, 'categories': Category.objects.all()})

def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    return render(request, 'parts/part_detail.html', {'part': part})

def parts_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    parts = Part.objects.filter(category=category)
    paginator = Paginator(parts, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'parts/part_list.html', {'parts': page_obj, 'categories': Category.objects.all(), 'selected_category': category})

def search_parts(request):
    query = request.GET.get('q', '')
    parts = Part.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Part.objects.none()
    paginator = Paginator(parts, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'parts/search.html', {'parts': page_obj, 'query': query})
