from django.contrib import admin
from .models import Category, Part, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'in_stock', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions = ['mark_out_of_stock', 'mark_in_stock']
    
    def mark_out_of_stock(self, request, queryset):
        queryset.update(stock=0)
    mark_out_of_stock.short_description = "Mark as Out of Stock"
    
    def mark_in_stock(self, request, queryset):
        queryset.update(stock=10)
    mark_in_stock.short_description = "Add 10 to Stock"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'part', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'part__name', 'title']
