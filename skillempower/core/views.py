from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, ProfileForm, CertificateUploadForm
from .models import Profile, BookmarkedCourse, Certificate, UserLessonProgress
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from instructors.models import Video, Course, Lesson, AssignmentSubmission
from django.urls import reverse
from django.shortcuts import render, redirect

@login_required
def profile_view(request):
    profile = request.user.profile
    certificates = Certificate.objects.filter(user=request.user)

    form = ProfileForm(instance=profile)
    certificate_form = CertificateUploadForm()

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'upload_certificate' in request.POST:
            certificate_form = CertificateUploadForm(request.POST, request.FILES)
            if certificate_form.is_valid():
                certificate = certificate_form.save(commit=False)
                certificate.user = request.user
                certificate.save()
                messages.success(request, 'Certificate uploaded successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')

    # Fetch user-specific data for the right side of the dashboard
    courses_taken = Course.objects.filter(instructor=request.user).count() # Assuming courses taken means courses created by instructor
    lessons_completed_count = UserLessonProgress.objects.filter(user=request.user).count()
    completed_lessons = UserLessonProgress.objects.filter(user=request.user).select_related('lesson', 'lesson__course').order_by('-completed_at')[:5] # Get last 5 completed lessons
    certificates_earned = Certificate.objects.filter(user=request.user).count()

    context = {
        'form': form,
        'certificate_form': certificate_form,
        'profile': profile,
        'courses_taken': courses_taken,
        'lessons_completed_count': lessons_completed_count,
        'certificates_earned': certificates_earned,
        'completed_lessons': completed_lessons,
        'certificates': certificates,
    }
    return render(request, 'core/profile.html', context)

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
            categories = [
                ('agro-based', 'Agro-based'),
                ('handicraft', 'Handicraft'),
                ('basic computer', 'Basic computer'),
                ('local food', 'Local Food'),
                ('design', 'Design & Fashion'),
                ('business', 'Business'),
                ('marketing', 'Marketing'),
            ]
        else:
            dashboard_type = 'Instructor/Admin'
            categories = []
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist (for backward compatibility)
        profile = Profile.objects.create(user=request.user, role='learner')
        dashboard_type = 'Learner'
        categories = [
            ('all', 'All Categories'),
            ('programming', 'Programming'),
            ('web-development', 'Web Development'),
            ('data-science', 'Data Science'),
            ('mobile-development', 'Mobile Development'),
            ('design', 'Design'),
            ('business', 'Business'),
            ('marketing', 'Marketing'),
        ]
    return render(request, 'core/dashboard.html', {'dashboard_type': dashboard_type, 'categories': categories})

# Course Search View
@login_required
def course_search_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    # Fetch videos from the database
    videos = Video.objects.all()
    if category and category != 'all':
        videos = videos.filter(category=category)
    if query:
        videos = videos.filter(title__icontains=query)

    # Get bookmarked video IDs for the current user
    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(BookmarkedCourse.objects.filter(user=request.user).values_list('video_id', flat=True))
    request.user.bookmarked_ids = bookmarked_ids

    dashboard_type = 'Learner' if request.user.profile.role == 'learner' else 'Instructor/Admin'

    context = {
        'courses': videos,
        'query': query,
        'category': category,
        'category_name': category,
        'total_results': videos.count(),
        'dashboard_type': dashboard_type,
    }
    return render(request, 'core/course_search.html', context)

@login_required
def bookmarked_videos_view(request):
    # Get all bookmarked video IDs for this user
    bookmarked_ids = BookmarkedCourse.objects.filter(user=request.user).values_list('video_id', flat=True)
    videos = Video.objects.filter(id__in=bookmarked_ids)
    request.user.bookmarked_ids = set(bookmarked_ids)
    context = {
        'courses': videos,
        'total_results': videos.count(),
        'dashboard_type': 'Learner' if request.user.profile.role == 'learner' else 'Instructor/Admin',
    }
    return render(request, 'core/bookmarked_videos.html', context)

@login_required
def bookmark_video_view(request, video_id):
    if request.method == 'POST':
        BookmarkedCourse.objects.get_or_create(user=request.user, video_id=video_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('course_search')))
