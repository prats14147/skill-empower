from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/')
    pdf_notes = models.FileField(upload_to='video_pdfs/', blank=True, null=True)
    assignment_link = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    playback_id = models.CharField(max_length=64, blank=True, null=True)  # Mux playback ID

    def __str__(self):
        return f"{self.title} by {self.instructor.username}"

class QuickLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='courses')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_no = models.PositiveIntegerField()
    video = models.FileField(upload_to='lesson_videos/')
    pdf_notes = models.FileField(upload_to='lesson_pdfs/', blank=True, null=True)
    assignment_description = models.TextField(blank=True)
    assignment_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'lesson_no')
        ordering = ['lesson_no']

    def __str__(self):
        return f"{self.course.title} - Lesson {self.lesson_no}: {self.title}"

class AssignmentSubmission(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.learner.username} - {self.lesson}"
