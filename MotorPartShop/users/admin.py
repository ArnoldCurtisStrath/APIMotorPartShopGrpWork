from django.contrib import admin

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['city', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number', 'address', 'city')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )