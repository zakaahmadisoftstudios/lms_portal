from rest_framework import generics, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db.models import Q

from .models import (
    Profile, Student, Teacher, Class, Subject, 
    Grade, Assignment, Attendance
)
from .serializers import (
    UserSerializer, ProfileSerializer, StudentSerializer, TeacherSerializer,
    ClassSerializer, SubjectSerializer, GradeSerializer, AssignmentSerializer,
    AttendanceSerializer, UserRegistrationSerializer, TeacherListSerializer,
    StudentListSerializer, UserToTeacherSerializer, UserToStudentSerializer
)
from .permissions import (
    IsAdminUser, IsTeacherUser, IsStaffUser, IsStudentUser,
    IsAdminOrTeacher, IsAdminOrReadOnly, StudentPermission,
    TeacherPermission, ClassPermission, AssignmentPermission,
    GradePermission, AttendancePermission
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that includes user profile information
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Add user profile info to response
            try:
                user = User.objects.get(username=request.data.get('username'))
                profile_data = ProfileSerializer(user.profile).data
                response.data['user'] = profile_data
            except User.DoesNotExist:
                pass
        return response


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_user(request):
    """
    Register a new user (Admin only)
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        profile_data = ProfileSerializer(user.profile).data
        return Response({
            'message': 'User created successfully',
            'user': profile_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_profile(request):
    """
    Get current logged-in user's profile
    """
    profile_data = ProfileSerializer(request.user.profile).data
    return Response(profile_data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for User management (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return User.objects.select_related('profile').all()


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student management with role-based access
    """
    queryset = Student.objects.all()
    permission_classes = [StudentPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer
    
    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        
        if role == 'admin':
            # Admin sees all students
            return Student.objects.select_related('user', 'class_enrolled').all()
        elif role == 'teacher':
            # Teacher sees students in their classes
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return Student.objects.filter(
                    class_enrolled__in=teacher_classes
                ).select_related('user', 'class_enrolled')
            return Student.objects.none()
        elif role == 'staff':
            # Staff sees all students (read-only via permissions)
            return Student.objects.select_related('user', 'class_enrolled').all()
        elif role == 'student':
            # Student sees only their own profile
            if hasattr(user, 'student_profile'):
                return Student.objects.filter(user=user)
            return Student.objects.none()
        
        return Student.objects.none()


class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Teacher management
    """
    queryset = Teacher.objects.all()
    permission_classes = [TeacherPermission]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherSerializer
    
    def get_queryset(self):
        return Teacher.objects.select_related('user').prefetch_related('subjects').all()
    
    @action(detail=True, methods=['get'])
    def classes(self, request, pk=None):
        """
        Get classes taught by a specific teacher
        """
        teacher = self.get_object()
        classes = teacher.classes.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Get students in classes taught by a specific teacher
        """
        teacher = self.get_object()
        students = Student.objects.filter(
            class_enrolled__teacher=teacher
        ).select_related('user', 'class_enrolled')
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)


class ClassViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Class management with role-based access
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [ClassPermission]
    
    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        
        if role == 'admin':
            # Admin sees all classes
            return Class.objects.select_related('teacher').prefetch_related('subjects').all()
        elif role == 'teacher':
            # Teacher sees only their assigned classes
            if hasattr(user, 'teacher_profile'):
                return Class.objects.filter(
                    teacher=user.teacher_profile
                ).select_related('teacher').prefetch_related('subjects')
            return Class.objects.none()
        elif role == 'student':
            # Student sees only their enrolled class
            if hasattr(user, 'student_profile'):
                enrolled_class = user.student_profile.class_enrolled
                if enrolled_class:
                    return Class.objects.filter(id=enrolled_class.id)
            return Class.objects.none()
        elif role == 'staff':
            # Staff has read-only access to all classes
            return Class.objects.select_related('teacher').prefetch_related('subjects').all()
        
        return Class.objects.none()


class SubjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Subject management
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Assignment management with role-based access
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentPermission]
    
    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        
        if role == 'admin':
            # Admin sees all assignments
            return Assignment.objects.select_related(
                'subject', 'class_assigned', 'teacher'
            ).all()
        elif role == 'teacher':
            # Teacher sees all assignments (can grade others)
            return Assignment.objects.select_related(
                'subject', 'class_assigned', 'teacher'
            ).all()
        elif role == 'student':
            # Student sees assignments for their class
            if hasattr(user, 'student_profile'):
                enrolled_class = user.student_profile.class_enrolled
                if enrolled_class:
                    return Assignment.objects.filter(
                        class_assigned=enrolled_class
                    ).select_related('subject', 'class_assigned', 'teacher')
            return Assignment.objects.none()
        
        return Assignment.objects.none()
    
    def perform_create(self, serializer):
        # Automatically set teacher for new assignments
        if hasattr(self.request.user, 'teacher_profile'):
            serializer.save(teacher=self.request.user.teacher_profile)
        else:
            serializer.save()


class GradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Grade management with role-based access
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [GradePermission]
    
    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        
        if role == 'admin':
            # Admin sees all grades
            return Grade.objects.select_related(
                'student__user', 'assignment', 'graded_by'
            ).all()
        elif role == 'teacher':
            # Teacher sees grades for students in their classes
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return Grade.objects.filter(
                    student__class_enrolled__in=teacher_classes
                ).select_related('student__user', 'assignment', 'graded_by')
            return Grade.objects.none()
        elif role == 'student':
            # Student sees only their own grades
            if hasattr(user, 'student_profile'):
                return Grade.objects.filter(
                    student=user.student_profile
                ).select_related('student__user', 'assignment', 'graded_by')
            return Grade.objects.none()
        
        return Grade.objects.none()
    
    def perform_create(self, serializer):
        # Automatically set graded_by for new grades
        if hasattr(self.request.user, 'teacher_profile'):
            serializer.save(graded_by=self.request.user.teacher_profile)
        else:
            serializer.save()


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Attendance management with role-based access
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AttendancePermission]
    
    def get_queryset(self):
        user = self.request.user
        role = user.profile.role
        
        if role == 'admin':
            # Admin sees all attendance records
            return Attendance.objects.select_related(
                'student__user', 'class_attended', 'subject', 'marked_by'
            ).all()
        elif role == 'teacher':
            # Teacher sees attendance for classes they teach
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return Attendance.objects.filter(
                    class_attended__in=teacher_classes
                ).select_related('student__user', 'class_attended', 'subject', 'marked_by')
            return Attendance.objects.none()
        elif role == 'student':
            # Student sees only their own attendance
            if hasattr(user, 'student_profile'):
                return Attendance.objects.filter(
                    student=user.student_profile
                ).select_related('student__user', 'class_attended', 'subject', 'marked_by')
            return Attendance.objects.none()
        
        return Attendance.objects.none()
    
    def perform_create(self, serializer):
        # Automatically set marked_by for new attendance records
        if hasattr(self.request.user, 'teacher_profile'):
            serializer.save(marked_by=self.request.user.teacher_profile)
        else:
            serializer.save()


# User conversion endpoints

@api_view(['POST'])
@permission_classes([IsAdminUser])
def convert_user_to_teacher(request):
    """
    Convert an existing user to a teacher (Admin only)
    """
    serializer = UserToTeacherSerializer(data=request.data)
    if serializer.is_valid():
        teacher = serializer.save()
        teacher_data = TeacherSerializer(teacher).data
        return Response({
            'message': 'User successfully converted to teacher',
            'teacher': teacher_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def convert_user_to_student(request):
    """
    Convert an existing user to a student (Admin only)
    """
    serializer = UserToStudentSerializer(data=request.data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data
        return Response({
            'message': 'User successfully converted to student',
            'student': student_data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Additional utility views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics based on user role
    """
    user = request.user
    role = user.profile.role
    stats = {}
    
    if role == 'admin':
        stats = {
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_classes': Class.objects.filter(is_active=True).count(),
            'total_subjects': Subject.objects.count(),
            'total_assignments': Assignment.objects.filter(is_active=True).count(),
        }
    elif role == 'teacher' and hasattr(user, 'teacher_profile'):
        teacher_classes = user.teacher_profile.classes.all()
        stats = {
            'my_classes': teacher_classes.count(),
            'my_students': Student.objects.filter(class_enrolled__in=teacher_classes).count(),
            'pending_assignments': Assignment.objects.filter(
                teacher=user.teacher_profile, 
                due_date__gte=timezone.now()
            ).count(),
            'subjects_teaching': user.teacher_profile.subjects.count(),
        }
    elif role == 'student' and hasattr(user, 'student_profile'):
        student = user.student_profile
        stats = {
            'my_class': student.class_enrolled.name if student.class_enrolled else 'Not assigned',
            'total_assignments': Assignment.objects.filter(
                class_assigned=student.class_enrolled
            ).count() if student.class_enrolled else 0,
            'completed_assignments': Grade.objects.filter(student=student).count(),
            'attendance_percentage': calculate_attendance_percentage(student),
        }
    
    return Response(stats)


def calculate_attendance_percentage(student):
    """
    Calculate attendance percentage for a student
    """
    total_days = Attendance.objects.filter(student=student).count()
    if total_days == 0:
        return 0
    present_days = Attendance.objects.filter(
        student=student, 
        status__in=['present', 'late']
    ).count()
    return round((present_days / total_days) * 100, 2)


# Import timezone for date operations
from django.utils import timezone


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    return Response({
        'status': 'healthy',
        'message': 'LMS Portal API is running',
        'version': '1.0.0',
        'timestamp': timezone.now().isoformat()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_endpoints(request):
    """
    List all available API endpoints
    """
    base_url = request.build_absolute_uri('/api/')
    
    endpoints = {
        'authentication': {
            'login': f'{base_url}auth/login/',
            'refresh_token': f'{base_url}auth/refresh/',
            'register': f'{base_url}auth/register/',
        },
        'user_profile': {
            'current_user': f'{base_url}profile/me/',
        },
        'dashboard': {
            'statistics': f'{base_url}dashboard/stats/',
        },
        'users': {
            'list': f'{base_url}users/',
            'detail': f'{base_url}users/{{id}}/',
            'convert_to_teacher': f'{base_url}users/convert-to-teacher/',
            'convert_to_student': f'{base_url}users/convert-to-student/',
        },
        'students': {
            'list': f'{base_url}students/',
            'create': f'{base_url}students/',
            'detail': f'{base_url}students/{{id}}/',
            'update': f'{base_url}students/{{id}}/',
            'delete': f'{base_url}students/{{id}}/',
        },
        'teachers': {
            'list': f'{base_url}teachers/',
            'create': f'{base_url}teachers/',
            'detail': f'{base_url}teachers/{{id}}/',
            'update': f'{base_url}teachers/{{id}}/',
            'delete': f'{base_url}teachers/{{id}}/',
            'teacher_classes': f'{base_url}teachers/{{id}}/classes/',
            'teacher_students': f'{base_url}teachers/{{id}}/students/',
        },
        'classes': {
            'list': f'{base_url}classes/',
            'create': f'{base_url}classes/',
            'detail': f'{base_url}classes/{{id}}/',
            'update': f'{base_url}classes/{{id}}/',
            'delete': f'{base_url}classes/{{id}}/',
        },
        'subjects': {
            'list': f'{base_url}subjects/',
            'create': f'{base_url}subjects/',
            'detail': f'{base_url}subjects/{{id}}/',
            'update': f'{base_url}subjects/{{id}}/',
            'delete': f'{base_url}subjects/{{id}}/',
        },
        'assignments': {
            'list': f'{base_url}assignments/',
            'create': f'{base_url}assignments/',
            'detail': f'{base_url}assignments/{{id}}/',
            'update': f'{base_url}assignments/{{id}}/',
            'delete': f'{base_url}assignments/{{id}}/',
        },
        'grades': {
            'list': f'{base_url}grades/',
            'create': f'{base_url}grades/',
            'detail': f'{base_url}grades/{{id}}/',
            'update': f'{base_url}grades/{{id}}/',
            'delete': f'{base_url}grades/{{id}}/',
        },
        'attendance': {
            'list': f'{base_url}attendance/',
            'create': f'{base_url}attendance/',
            'detail': f'{base_url}attendance/{{id}}/',
            'update': f'{base_url}attendance/{{id}}/',
            'delete': f'{base_url}attendance/{{id}}/',
        },
    }
    
    return Response({
        'message': 'LMS Portal API v1',
        'version': '1.0.0',
        'endpoints': endpoints,
        'authentication': {
            'type': 'JWT Bearer Token',
            'header': 'Authorization: Bearer <token>',
            'obtain_token': f'{base_url}auth/login/',
        },
        'permissions': {
            'admin': 'Full access to all resources',
            'teacher': 'Access to assigned classes, students, and grading',
            'student': 'Read-only access to own data',
            'staff': 'Read-only access to most resources',
        }
    })
