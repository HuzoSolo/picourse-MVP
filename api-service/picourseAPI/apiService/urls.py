from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='user-register'),
    path('auth/login/', views.login, name='user-login'),
    
    # User profile endpoints
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Subject endpoints
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    
    # Tutor endpoints
    path('tutors/', views.TutorListView.as_view(), name='tutor-list'),
    path('tutors/<int:pk>/', views.TutorDetailView.as_view(), name='tutor-detail'),
    
    # Lesson request endpoints
    path('lesson-requests/', views.LessonRequestListView.as_view(), name='lesson-request-list'),
    path('lesson-requests/create/', views.LessonRequestCreateView.as_view(), name='lesson-request-create'),
    path('lesson-requests/<int:pk>/', views.LessonRequestUpdateView.as_view(), name='lesson-request-update'),
]
