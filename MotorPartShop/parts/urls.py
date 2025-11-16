
from django.urls import path
from . import views, review_views

app_name = 'parts'

urlpatterns = [
    path('', views.part_list, name='list'),
    path('search/', views.search_parts, name='search'),
    path('<int:pk>/', views.part_detail, name='detail'),
    path('category/<int:category_id>/', views.parts_by_category, name='by_category'),
    path('<int:part_id>/review/', review_views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', review_views.delete_review, name='delete_review'),
]
