from django.contrib import admin
from .models import QuickLink, Course, Lesson, AssignmentSubmission

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')
    inlines = [LessonInline]
    search_fields = ('title', 'instructor__username')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson_no')
    list_filter = ('course',)
    ordering = ('course', 'lesson_no')

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'learner', 'submitted_at')
    search_fields = ('lesson__title', 'learner__username')
