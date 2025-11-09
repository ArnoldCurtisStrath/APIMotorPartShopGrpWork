from django.shortcuts import render, get_object_or_404

from .models import Category, Part



def part_list(request):
    parts = Part.objects.select_related('category').all()
    categories = Category.objects.all()
    context = {
        'parts': parts,
        'categories': categories,
        'selected_category': None,
    }
    return render(request, 'parts/part_list.html', context)



def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    return render(request, 'parts/part_detail.html', {'part': part})



def parts_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    parts = Part.objects.filter(category=category).select_related('category')
    categories = Category.objects.all()
    context = {
        'parts': parts,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'parts/part_list.html', context)
