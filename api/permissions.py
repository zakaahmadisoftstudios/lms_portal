from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Permission to check if user is admin
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'admin'
        )


class IsTeacherUser(BasePermission):
    """
    Permission to check if user is teacher
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'teacher'
        )


class IsStaffUser(BasePermission):
    """
    Permission to check if user is staff
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'staff'
        )


class IsStudentUser(BasePermission):
    """
    Permission to check if user is student
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'student'
        )


class IsAdminOrTeacher(BasePermission):
    """
    Permission to check if user is admin or teacher
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role in ['admin', 'teacher']
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to allow admin full access and others read-only
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == 'admin'
        )


class StudentPermission(BasePermission):
    """
    Custom permission for student-related operations
    - Admin: Full access
    - Teacher: Access to students in their classes
    - Staff: Limited access to student data
    - Student: Only their own profile
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can view/edit students in their classes
        if role == 'teacher':
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return obj.class_enrolled in teacher_classes
            return False
            
        # Staff has read-only access to student data
        if role == 'staff':
            return request.method in SAFE_METHODS
            
        # Student can only access their own profile
        if role == 'student':
            return obj.user == user
            
        return False


class TeacherPermission(BasePermission):
    """
    Custom permission for teacher-related operations
    - Admin: Full access
    - Teacher: Access to their own profile
    - Others: Read-only access to basic teacher info
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can edit their own profile
        if role == 'teacher':
            if request.method in SAFE_METHODS:
                return True
            return obj.user == user
            
        # Others have read-only access
        return request.method in SAFE_METHODS


class ClassPermission(BasePermission):
    """
    Custom permission for class-related operations
    - Admin: Full access
    - Teacher: Access to their assigned classes
    - Student: Read-only access to their enrolled class
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can access their assigned classes
        if role == 'teacher':
            if hasattr(user, 'teacher_profile'):
                return obj.teacher == user.teacher_profile
            return False
            
        # Student has read-only access to their enrolled class
        if role == 'student':
            if request.method in SAFE_METHODS and hasattr(user, 'student_profile'):
                return obj == user.student_profile.class_enrolled
            return False
            
        # Staff has read-only access
        if role == 'staff':
            return request.method in SAFE_METHODS
            
        return False


class AssignmentPermission(BasePermission):
    """
    Custom permission for assignment-related operations
    - Admin: Full access
    - Teacher: Create assignments for their classes, edit their own assignments
    - Student: Read-only access to assignments for their class
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can edit their own assignments
        if role == 'teacher':
            if hasattr(user, 'teacher_profile'):
                return obj.teacher == user.teacher_profile
            return False
            
        # Student has read-only access to their class assignments
        if role == 'student':
            if request.method in SAFE_METHODS and hasattr(user, 'student_profile'):
                return obj.class_assigned == user.student_profile.class_enrolled
            return False
            
        return False


class GradePermission(BasePermission):
    """
    Custom permission for grade-related operations
    - Admin: Full access
    - Teacher: Create/edit grades for students in their classes
    - Student: Read-only access to their own grades
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can grade students in their classes
        if role == 'teacher':
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return obj.student.class_enrolled in teacher_classes
            return False
            
        # Student can only view their own grades
        if role == 'student':
            if request.method in SAFE_METHODS and hasattr(user, 'student_profile'):
                return obj.student == user.student_profile
            return False
            
        return False


class AttendancePermission(BasePermission):
    """
    Custom permission for attendance-related operations
    - Admin: Full access
    - Teacher: Mark attendance for students in their classes
    - Student: Read-only access to their own attendance
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not hasattr(user, 'profile'):
            return False
            
        role = user.profile.role
        
        # Admin has full access
        if role == 'admin':
            return True
            
        # Teacher can mark attendance for students in their classes
        if role == 'teacher':
            if hasattr(user, 'teacher_profile'):
                teacher_classes = user.teacher_profile.classes.all()
                return obj.class_attended in teacher_classes
            return False
            
        # Student can only view their own attendance
        if role == 'student':
            if request.method in SAFE_METHODS and hasattr(user, 'student_profile'):
                return obj.student == user.student_profile
            return False
            
        return False 