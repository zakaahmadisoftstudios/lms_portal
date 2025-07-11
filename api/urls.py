from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView, register_user, current_user_profile,
    UserViewSet, StudentViewSet, TeacherViewSet, ClassViewSet,
    SubjectViewSet, AssignmentViewSet, GradeViewSet, AttendanceViewSet,
    dashboard_stats, api_endpoints, health_check, convert_user_to_teacher,
    convert_user_to_student
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# API v1 URL patterns
v1_patterns = [
    # API Documentation and Health
    path('', api_endpoints, name='api_root'),
    path('endpoints/', api_endpoints, name='api_endpoints'),
    path('health/', health_check, name='health_check'),
    
    # Authentication endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/register/', register_user, name='auth_register'),
    
    # User profile endpoints
    path('profile/me/', current_user_profile, name='user_profile'),
    
    # User conversion endpoints
    path('users/convert-to-teacher/', convert_user_to_teacher, name='convert_user_to_teacher'),
    path('users/convert-to-student/', convert_user_to_student, name='convert_user_to_student'),
    
    # Dashboard endpoints
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    
    # Core resource endpoints
    path('', include(router.urls)),
]

# Main URL patterns with versioning
urlpatterns = [
    # API versioning
    path('v1/', include(v1_patterns)),
    
    # Default to v1 (backward compatibility)
    path('', include(v1_patterns)),
] 