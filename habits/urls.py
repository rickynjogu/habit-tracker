from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('habit/create/', views.habit_create, name='habit_create'),
    path('habit/<int:pk>/edit/', views.habit_update, name='habit_update'),
    path('habit/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habit/<int:pk>/toggle/', views.toggle_habit, name='toggle_habit'),
    path('habit/<int:pk>/analytics/', views.analytics, name='habit_analytics'),
]
