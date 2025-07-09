from django import forms
from .models import Video, Course, Lesson

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video', 'pdf_notes', 'assignment_link']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'lesson_no', 'video', 'pdf_notes', 'assignment_description', 'assignment_link'] 