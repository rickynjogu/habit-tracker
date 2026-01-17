from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class Habit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    color = models.CharField(max_length=7, default='#6366f1', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)
    target_days_per_week = models.IntegerField(default=7, help_text='Target days per week')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_current_streak(self):
        """Calculate current streak in days"""
        entries = self.entries.order_by('-date')
        if not entries.exists():
            return 0
        
        today = timezone.now().date()
        streak = 0
        
        # Check if today is completed
        if entries.first().date == today:
            streak = 1
            check_date = today - timedelta(days=1)
        else:
            check_date = today - timedelta(days=1)
        
        # Count consecutive days
        for entry in entries[1:]:
            if entry.date == check_date:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_longest_streak(self):
        """Calculate longest streak ever"""
        entries = self.entries.order_by('date')
        if not entries.exists():
            return 0
        
        longest_streak = 1
        current_streak = 1
        prev_date = entries.first().date
        
        for entry in entries[1:]:
            if entry.date == prev_date + timedelta(days=1):
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
            prev_date = entry.date
        
        return max(longest_streak, current_streak)
    
    def get_completion_rate(self, days=30):
        """Get completion rate for the last N days"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days-1)
        entries_count = self.entries.filter(date__gte=start_date, date__lte=end_date).count()
        return round((entries_count / days) * 100, 1)
    
    def is_completed_today(self):
        """Check if habit is completed today"""
        today = timezone.now().date()
        return self.entries.filter(date=today).exists()


class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.habit.name} - {self.date}"
