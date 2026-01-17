from django.contrib import admin
from .models import Habit, HabitEntry


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at', 'get_current_streak', 'get_longest_streak']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def get_current_streak(self, obj):
        return obj.get_current_streak()
    get_current_streak.short_description = 'Current Streak'


@admin.register(HabitEntry)
class HabitEntryAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['habit__name', 'notes']
    readonly_fields = ['created_at']
