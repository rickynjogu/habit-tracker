# 🎯 Habit Tracker - Smart Django Application

A beautiful, feature-rich habit tracking application built with Django. Track your daily habits, monitor streaks, and visualize your progress with analytics!

## ✨ Features

- **User Authentication** - Secure registration and login system
- **Habit Management** - Create, edit, and delete habits with custom colors
- **Daily Tracking** - Mark habits as completed with a single click
- **Streak Tracking** - Monitor current and longest streaks for motivation
- **Analytics Dashboard** - Visualize your progress with interactive charts
- **30-Day Calendar** - See your completion history at a glance
- **Weekly Breakdown** - Track weekly performance statistics
- **Modern UI** - Beautiful, responsive design with Bootstrap 5
- **Completion Rates** - Track your progress over 7 and 30-day periods

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd testproject
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

## 📖 Usage

### Getting Started

1. **Register** - Create a new account on the registration page
2. **Login** - Sign in to access your dashboard
3. **Create Habits** - Click "Add New Habit" to create your first habit
4. **Track Daily** - Click the checkbox on each habit card to mark it as complete
5. **View Analytics** - Click the analytics icon to see detailed progress charts

### Features Overview

- **Dashboard**: View all your habits with current streaks and completion rates
- **Create/Edit Habits**: Customize habits with names, descriptions, colors, and target days per week
- **Daily Tracking**: Toggle habits on/off by clicking the checkbox
- **Analytics**: See detailed statistics including:
  - Current streak
  - Longest streak ever
  - 7-day completion rate
  - 30-day completion rate
  - Interactive calendar view
  - Weekly breakdown table

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: Bootstrap 5.3.0, Bootstrap Icons
- **Charts**: Chart.js 4.4.0
- **Database**: SQLite (default, can be changed for production)

## 📁 Project Structure

```
habit_tracker/
├── habit_tracker/          # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── ...
├── habits/                 # Main app
│   ├── models.py          # Habit and HabitEntry models
│   ├── views.py           # View functions
│   ├── forms.py           # Form classes
│   ├── urls.py            # App URL configuration
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
│       └── habits/
│           ├── base.html
│           ├── dashboard.html
│           ├── login.html
│           └── ...
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Customization

### Changing Colors

Each habit has a customizable color. When creating or editing a habit, use the color picker to choose your preferred color.

### Target Days Per Week

Set how many days per week you want to maintain each habit. Default is 7 days.

## 📊 Database Models

- **Habit**: Stores habit information (name, description, color, target days)
- **HabitEntry**: Tracks daily completions (links habit to date)

## 🔒 Security Notes

- This is a development version with `DEBUG = True`
- For production, update `SECRET_KEY` and set `DEBUG = False`
- Consider using a production database (PostgreSQL, MySQL, etc.)
- Configure proper static files handling for production

## 🤝 Contributing

Feel free to fork this project and make it your own! Add features like:
- Reminders/notifications
- Habit categories
- Social sharing
- Mobile app version
- Export data functionality

## 📝 License

This project is open source and available for learning purposes.

## 💡 Tips

- Start with 2-3 habits to build consistency
- Check off habits at the same time each day
- Use the analytics to identify patterns
- Celebrate your streaks!

---

**Enjoy building better habits! 🚀**
