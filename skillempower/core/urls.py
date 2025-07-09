from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('courses/search/', views.course_search_view, name='course_search'),
    path('bookmarks/', views.bookmarked_videos_view, name='bookmarked_videos'),
    path('bookmark/<int:video_id>/', views.bookmark_video_view, name='bookmark_video'),
    path('profile/', views.profile_view, name='profile'),
] 