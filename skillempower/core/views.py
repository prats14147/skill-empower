from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.

# Home page view
def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

# User Registration View
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/signup.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# User Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.role == 'learner':
            dashboard_type = 'Learner'
        else:
            dashboard_type = 'Instructor/Admin'
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist (for backward compatibility)
        profile = Profile.objects.create(user=request.user, role='learner')
        dashboard_type = 'Learner'
    
    return render(request, 'core/dashboard.html', {'dashboard_type': dashboard_type})

# Course Search View
@login_required
def course_search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    
    # Mock course data with categories - in a real application, this would come from a database
    mock_courses = [
        {
            'id': 1,
            'title': 'Python Programming for Beginners',
            'description': 'Learn Python from scratch with hands-on projects',
            'instructor': 'Dr. Sarah Johnson',
            'duration': '8 weeks',
            'level': 'Beginner',
            'rating': 4.8,
            'students': 1250,
            'category': 'programming'
        },
        {
            'id': 2,
            'title': 'Advanced Web Development',
            'description': 'Master modern web development with React and Node.js',
            'instructor': 'Prof. Michael Chen',
            'duration': '12 weeks',
            'level': 'Advanced',
            'rating': 4.9,
            'students': 890,
            'category': 'web-development'
        },
        {
            'id': 3,
            'title': 'Data Science Fundamentals',
            'description': 'Introduction to data analysis and machine learning',
            'instructor': 'Dr. Emily Rodriguez',
            'duration': '10 weeks',
            'level': 'Intermediate',
            'rating': 4.7,
            'students': 2100,
            'category': 'data-science'
        },
        {
            'id': 4,
            'title': 'Mobile App Development',
            'description': 'Build iOS and Android apps with Flutter',
            'instructor': 'Alex Thompson',
            'duration': '14 weeks',
            'level': 'Intermediate',
            'rating': 4.6,
            'students': 750,
            'category': 'mobile-development'
        },
        {
            'id': 5,
            'title': 'UI/UX Design Masterclass',
            'description': 'Create beautiful and functional user interfaces',
            'instructor': 'Lisa Wang',
            'duration': '6 weeks',
            'level': 'Beginner',
            'rating': 4.5,
            'students': 1200,
            'category': 'design'
        },
        {
            'id': 6,
            'title': 'Digital Marketing Strategy',
            'description': 'Learn modern marketing techniques and strategies',
            'instructor': 'David Kim',
            'duration': '8 weeks',
            'level': 'Intermediate',
            'rating': 4.4,
            'students': 950,
            'category': 'marketing'
        },
        {
            'id': 7,
            'title': 'Business Analytics',
            'description': 'Transform data into business insights',
            'instructor': 'Maria Garcia',
            'duration': '10 weeks',
            'level': 'Advanced',
            'rating': 4.6,
            'students': 680,
            'category': 'business'
        },
        {
            'id': 8,
            'title': 'JavaScript Fundamentals',
            'description': 'Master JavaScript programming from basics to advanced',
            'instructor': 'John Smith',
            'duration': '9 weeks',
            'level': 'Beginner',
            'rating': 4.7,
            'students': 1800,
            'category': 'programming'
        }
    ]
    
    # Filter courses based on search query and category
    filtered_courses = mock_courses
    
    # Apply category filter
    if category and category != 'all':
        filtered_courses = [course for course in filtered_courses if course['category'] == category]
    
    # Apply text search filter
    if query:
        filtered_courses = [
            course for course in filtered_courses
            if query.lower() in course['title'].lower() or 
               query.lower() in course['description'].lower() or
               query.lower() in course['instructor'].lower()
        ]
    
    # Category mapping for display
    category_names = {
        'programming': 'Programming',
        'web-development': 'Web Development',
        'data-science': 'Data Science',
        'mobile-development': 'Mobile Development',
        'design': 'Design',
        'business': 'Business',
        'marketing': 'Marketing'
    }
    
    context = {
        'courses': filtered_courses,
        'query': query,
        'category': category,
        'category_name': category_names.get(category, 'All Categories'),
        'total_results': len(filtered_courses)
    }
    
    return render(request, 'core/course_search.html', context)
