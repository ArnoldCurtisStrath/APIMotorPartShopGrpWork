from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Part, Review
from .forms import ReviewForm

@login_required
def add_review(request, part_id):
    part = get_object_or_404(Part, pk=part_id)
    
    if Review.objects.filter(part=part, user=request.user).exists():
        messages.warning(request, 'You already reviewed this part.')
        return redirect('parts:detail', pk=part_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.part = part
            review.user = request.user
            review.save()
            messages.success(request, 'Review added!')
            return redirect('parts:detail', pk=part_id)
    else:
        form = ReviewForm()
    
    return render(request, 'parts/add_review.html', {'form': form, 'part': part})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    part_id = review.part.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('parts:detail', pk=part_id)
    return render(request, 'parts/delete_review.html', {'review': review})
