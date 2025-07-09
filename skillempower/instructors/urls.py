from django.urls import path
from . import views

app_name = 'instructors'

urlpatterns = [
    path('upload-video/', views.video_upload_view, name='video_upload'),
    path('uploads/', views.uploads_dashboard, name='uploads_dashboard'),
    path('create-course/', views.create_course_view, name='create_course'),
    path('course/<int:course_id>/add-lesson/', views.add_lesson_view, name='add_lesson'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('delete-video/<int:video_id>/', views.delete_video_view, name='delete_video'),
] 