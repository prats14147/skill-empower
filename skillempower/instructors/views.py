from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VideoUploadForm, CourseForm, LessonForm
from .models import Video, Course, Lesson, QuickLink, Category
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

def is_instructor(user):
    return hasattr(user, 'profile') and user.profile.role == 'instructor'

@login_required
@user_passes_test(is_instructor)
def video_upload_view(request):
    selected_category = request.GET.get('category')
    courses = Course.objects.filter(instructor=request.user)
    category_courses = []
    if selected_category:
        category_courses = courses.filter(category=selected_category)

    if request.method == 'POST' and 'create_course' in request.POST:
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructors:video_upload')
    else:
        course_form = CourseForm()

    context = {
        'course_form': course_form,
        'category_courses': category_courses,
        'selected_category': selected_category,
        'categories': Course.CATEGORY_CHOICES,
    }
    return render(request, 'instructors/instructor_video_upload.html', context)



@login_required
@user_passes_test(is_instructor)
def uploads_dashboard(request):
    quick_links = QuickLink.objects.all()
    courses = Course.objects.filter(instructor=request.user)
    course_form = CourseForm()
    lesson_form = LessonForm()
    selected_course = None
    lessons = None

    # Fetch only videos uploaded by this instructor
    my_videos = Video.objects.filter(instructor=request.user)

    # Handle course creation
    if request.method == 'POST' and 'create_course' in request.POST:
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.instructor = request.user
            new_course.save()
            return redirect('instructors:uploads_dashboard')

    # Handle lesson creation
    if request.method == 'POST' and 'create_lesson' in request.POST:
        lesson_form = LessonForm(request.POST, request.FILES)
        course_id = request.POST.get('course_id')
        if lesson_form.is_valid() and course_id:
            lesson = lesson_form.save(commit=False)
            lesson.course_id = course_id
            lesson.save()
            return redirect('instructors:uploads_dashboard')

    # If a course is selected, show its lessons
    course_id = request.GET.get('course')
    if course_id:
        selected_course = Course.objects.get(id=course_id, instructor=request.user)
        lessons = selected_course.lessons.all()

    context = {
        'quick_links': quick_links,
        'courses': courses,
        'course_form': course_form,
        'lesson_form': lesson_form,
        'selected_course': selected_course,
        'lessons': lessons,
        'my_videos': my_videos,  # Added to context
    }
    return render(request, 'instructors/uploads_dashboard.html', context)


@login_required
@user_passes_test(is_instructor)
def create_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructors:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'instructors/create_course.html', {'form': form})

@login_required
@user_passes_test(is_instructor)
def add_lesson_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson added successfully!')
            return redirect('instructors:course_detail', course_id=course.id)
    else:
        form = LessonForm()
    return render(request, 'instructors/add_lesson.html', {'form': form, 'course': course})

@login_required
@user_passes_test(is_instructor)
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    lessons = course.lessons.all()
    return render(request, 'instructors/course_detail.html', {'course': course, 'lessons': lessons})


@login_required
@user_passes_test(is_instructor)
def delete_video_view(request, video_id):
    video = get_object_or_404(Video, id=video_id, instructor=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('instructors:uploads_dashboard')))
    return render(request, 'instructors/confirm_delete_video.html', {'video': video})
