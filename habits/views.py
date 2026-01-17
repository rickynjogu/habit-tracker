from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Habit, HabitEntry
from .forms import HabitForm
import json


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'habits/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'habits/login.html')


@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    
    # Get today's date
    today = timezone.now().date()
    
    # Calculate statistics
    total_habits = habits.count()
    completed_today = sum(1 for habit in habits if habit.is_completed_today())
    
    # Get recent entries for calendar view
    recent_entries = HabitEntry.objects.filter(
        habit__user=request.user,
        date__gte=today - timedelta(days=7)
    ).order_by('-date')
    
    context = {
        'habits': habits,
        'today': today,
        'total_habits': total_habits,
        'completed_today': completed_today,
        'recent_entries': recent_entries,
    }
    return render(request, 'habits/dashboard.html', context)


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f'Habit "{habit.name}" created successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Create New Habit'})


@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Habit "{habit.name}" updated successfully!')
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'habit': habit, 'title': 'Edit Habit'})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit_name = habit.name
        habit.delete()
        messages.success(request, f'Habit "{habit_name}" deleted successfully!')
        return redirect('dashboard')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})


@login_required
@require_POST
def toggle_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    
    entry, created = HabitEntry.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'notes': ''}
    )
    
    if not created:
        entry.delete()
        completed = False
    else:
        completed = True
    
    return JsonResponse({
        'completed': completed,
        'streak': habit.get_current_streak(),
        'longest_streak': habit.get_longest_streak(),
        'completion_rate': habit.get_completion_rate(30)
    })


@login_required
def analytics(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    
    # Get data for last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=29)
    
    # Create date range
    date_range = [start_date + timedelta(days=x) for x in range(30)]
    
    # Get entries
    entries = HabitEntry.objects.filter(
        habit=habit,
        date__gte=start_date,
        date__lte=end_date
    ).values_list('date', flat=True)
    
    # Create completion data
    completion_data = []
    for date in date_range:
        completion_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'completed': date in entries,
            'day_name': date.strftime('%a')
        })
    
    # Weekly statistics
    weeks_data = []
    for week_start in range(0, 30, 7):
        week_end = min(week_start + 6, 29)
        week_dates = date_range[week_start:week_end+1]
        week_entries = sum(1 for date in week_dates if date in entries)
        weeks_data.append({
            'week': len(weeks_data) + 1,
            'completed': week_entries,
            'total': len(week_dates),
            'percentage': round((week_entries / len(week_dates)) * 100, 1)
        })
    
    context = {
        'habit': habit,
        'completion_data': json.dumps(completion_data),
        'weeks_data': weeks_data,
        'current_streak': habit.get_current_streak(),
        'longest_streak': habit.get_longest_streak(),
        'completion_rate_30': habit.get_completion_rate(30),
        'completion_rate_7': habit.get_completion_rate(7),
    }
    return render(request, 'habits/analytics.html', context)
