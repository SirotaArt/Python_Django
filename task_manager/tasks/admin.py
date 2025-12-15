from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'status', 'user', 'created_at', 'deadline']
    list_filter = ['status', 'category', 'priority', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'priority')
        }),
        ('Статус и сроки', {
            'fields': ('status', 'deadline', 'user')
        }),
    )