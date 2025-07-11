from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Profile, Student, Teacher, Class, Subject, 
    Grade, Assignment, Attendance
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'role_display', 'phone_number', 'address', 
                 'date_of_birth', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'credits', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_id', 'employee_id', 'department', 'qualification', 
                 'experience_years', 'specialization', 'subjects', 'subject_ids',
                 'hire_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_user_id(self, value):
        """Validate that the user exists and doesn't already have a teacher profile"""
        if value:
            try:
                user = User.objects.get(id=value)
                if hasattr(user, 'teacher_profile'):
                    raise serializers.ValidationError("User already has a teacher profile")
                return value
            except User.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
        return value
    
    def create(self, validated_data):
        subject_ids = validated_data.pop('subject_ids', [])
        # user_id is now required, so it will always be present
        teacher = Teacher.objects.create(**validated_data)
        if subject_ids:
            teacher.subjects.set(subject_ids)
        return teacher
    
    def update(self, instance, validated_data):
        subject_ids = validated_data.pop('subject_ids', None)
        # Remove user_id from update data to prevent changing user association
        validated_data.pop('user_id', None)
        instance = super().update(instance, validated_data)
        if subject_ids is not None:
            instance.subjects.set(subject_ids)
        return instance


class ClassSerializer(serializers.ModelSerializer):
    """Serializer for Class model"""
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'name', 'grade_level', 'section', 'academic_year', 
                 'teacher', 'teacher_id', 'subjects', 'subject_ids', 'room_number', 
                 'max_students', 'student_count', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.students.filter(is_active=True).count()
    
    def create(self, validated_data):
        subject_ids = validated_data.pop('subject_ids', [])
        class_obj = Class.objects.create(**validated_data)
        if subject_ids:
            class_obj.subjects.set(subject_ids)
        return class_obj
    
    def update(self, instance, validated_data):
        subject_ids = validated_data.pop('subject_ids', None)
        instance = super().update(instance, validated_data)
        if subject_ids is not None:
            instance.subjects.set(subject_ids)
        return instance


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
    class_enrolled = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'user_id', 'student_id', 'roll_number', 'class_enrolled', 'class_id',
                 'gender', 'gender_display', 'guardian_name', 'guardian_phone', 
                 'guardian_email', 'emergency_contact', 'admission_date', 
                 'blood_group', 'medical_conditions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_user_id(self, value):
        """Validate that the user exists and doesn't already have a student profile"""
        if value:
            try:
                user = User.objects.get(id=value)
                if hasattr(user, 'student_profile'):
                    raise serializers.ValidationError("User already has a student profile")
                return value
            except User.DoesNotExist:
                raise serializers.ValidationError("User does not exist")
        return value
    
    def create(self, validated_data):
        class_id = validated_data.pop('class_id', None)
        
        # Map class_id to class_enrolled_id if provided
        if class_id:
            validated_data['class_enrolled_id'] = class_id
        
        # user_id is now required, so it will always be present
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Remove user_id from update data to prevent changing user association
        validated_data.pop('user_id', None)
        return super().update(instance, validated_data)


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment model"""
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    class_assigned = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True)
    teacher = TeacherSerializer(read_only=True)
    assignment_type_display = serializers.CharField(source='get_assignment_type_display', read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'subject_id', 
                 'class_assigned', 'class_id', 'teacher', 'assignment_type', 
                 'assignment_type_display', 'total_marks', 'due_date', 
                 'instructions', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['teacher', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set teacher from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'teacher_profile'):
            validated_data['teacher'] = request.user.teacher_profile
        return super().create(validated_data)


class GradeSerializer(serializers.ModelSerializer):
    """Serializer for Grade model"""
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    assignment = AssignmentSerializer(read_only=True)
    assignment_id = serializers.IntegerField(write_only=True)
    graded_by = TeacherSerializer(read_only=True)
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_id', 'assignment', 'assignment_id',
                 'marks_obtained', 'grade_letter', 'percentage', 'comments', 
                 'submitted_date', 'graded_date', 'graded_by']
        read_only_fields = ['grade_letter', 'graded_date', 'graded_by']
    
    def get_percentage(self, obj):
        return round(obj.calculate_percentage(), 2)
    
    def create(self, validated_data):
        # Set graded_by from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'teacher_profile'):
            validated_data['graded_by'] = request.user.teacher_profile
        return super().create(validated_data)
    
    def validate_marks_obtained(self, value):
        # Get assignment_id from initial data safely
        assignment_id = None
        if hasattr(self, 'initial_data') and self.initial_data:
            assignment_id = self.initial_data.get('assignment_id')
        
        if assignment_id:
            try:
                assignment = Assignment.objects.get(id=assignment_id)
                if value > assignment.total_marks:
                    raise serializers.ValidationError(
                        f"Marks obtained cannot exceed total marks ({assignment.total_marks})"
                    )
            except (Assignment.DoesNotExist, ObjectDoesNotExist):
                # Assignment doesn't exist, validation will be handled elsewhere
                pass
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    class_attended = ClassSerializer(read_only=True)
    class_id = serializers.IntegerField(write_only=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    marked_by = TeacherSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_id', 'class_attended', 'class_id',
                 'subject', 'subject_id', 'date', 'status', 'status_display',
                 'marked_by', 'notes', 'marked_at']
        read_only_fields = ['marked_by', 'marked_at']
    
    def create(self, validated_data):
        # Set marked_by from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'teacher_profile'):
            validated_data['marked_by'] = request.user.teacher_profile
        return super().create(validated_data)


# Simplified serializers for listing
class TeacherListSerializer(serializers.ModelSerializer):
    """Simplified serializer for teacher listing"""
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'employee_id', 'department', 'specialization']


class StudentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for student listing"""
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class_name = serializers.CharField(source='class_enrolled.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'student_id', 'roll_number', 'class_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Enhanced serializer for user registration with automatic Teacher/Student creation"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    
    # Teacher specific fields
    employee_id = serializers.CharField(write_only=True, required=False)
    department = serializers.CharField(write_only=True, required=False)
    qualification = serializers.CharField(write_only=True, required=False)
    experience_years = serializers.IntegerField(write_only=True, required=False, default=0)
    specialization = serializers.CharField(write_only=True, required=False)
    hire_date = serializers.DateField(write_only=True, required=False)
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    # Student specific fields
    student_id = serializers.CharField(write_only=True, required=False)
    roll_number = serializers.CharField(write_only=True, required=False)
    class_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=Student.GENDER_CHOICES, write_only=True, required=False)
    guardian_name = serializers.CharField(write_only=True, required=False)
    guardian_phone = serializers.CharField(write_only=True, required=False)
    guardian_email = serializers.EmailField(write_only=True, required=False)
    emergency_contact = serializers.CharField(write_only=True, required=False)
    admission_date = serializers.DateField(write_only=True, required=False)
    blood_group = serializers.CharField(write_only=True, required=False)
    medical_conditions = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'role',
            # Teacher fields
            'employee_id', 'department', 'qualification', 'experience_years', 'specialization', 
            'hire_date', 'subject_ids',
            # Student fields
            'student_id', 'roll_number', 'class_id', 'gender', 'guardian_name', 'guardian_phone',
            'guardian_email', 'emergency_contact', 'admission_date', 'blood_group', 'medical_conditions'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        
        role = attrs.get('role')
        
        # Validate teacher-specific required fields
        if role == 'teacher':
            required_teacher_fields = ['employee_id', 'department', 'qualification', 'hire_date']
            for field in required_teacher_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required for teacher registration")
        
        # Validate student-specific required fields
        elif role == 'student':
            required_student_fields = ['student_id', 'roll_number', 'gender', 'guardian_name', 'guardian_phone', 'admission_date']
            for field in required_student_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required for student registration")
        
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        # Extract teacher/student specific data
        teacher_data = {}
        student_data = {}
        subject_ids = validated_data.pop('subject_ids', [])
        
        if role == 'teacher':
            teacher_fields = ['employee_id', 'department', 'qualification', 'experience_years', 'specialization', 'hire_date']
            for field in teacher_fields:
                if field in validated_data:
                    teacher_data[field] = validated_data.pop(field)
        
        elif role == 'student':
            student_fields = ['student_id', 'roll_number', 'class_id', 'gender', 'guardian_name', 'guardian_phone',
                            'guardian_email', 'emergency_contact', 'admission_date', 'blood_group', 'medical_conditions']
            for field in student_fields:
                if field in validated_data:
                    student_data[field] = validated_data.pop(field)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Update the profile role
        profile = user.profile
        profile.role = role
        profile.save()
        
        # Create Teacher or Student object if needed
        if role == 'teacher' and teacher_data:
            teacher = Teacher.objects.create(user=user, **teacher_data)
            if subject_ids:
                teacher.subjects.set(subject_ids)
        
        elif role == 'student' and student_data:
            Student.objects.create(user=user, **student_data)
        
        return user


# User conversion serializers
class UserToTeacherSerializer(serializers.ModelSerializer):
    """Serializer to convert existing user to teacher"""
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Teacher
        fields = ['user_id', 'employee_id', 'department', 'qualification', 'experience_years', 
                 'specialization', 'hire_date', 'is_active']
    
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            if hasattr(user, 'teacher_profile'):
                raise serializers.ValidationError("User already has a teacher profile")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        
        # Update user's profile role
        profile = user.profile
        profile.role = 'teacher'
        profile.save()
        
        return Teacher.objects.create(user=user, **validated_data)


class UserToStudentSerializer(serializers.ModelSerializer):
    """Serializer to convert existing user to student"""
    user_id = serializers.IntegerField()
    
    class Meta:
        model = Student
        fields = ['user_id', 'student_id', 'roll_number', 'class_id', 'gender', 'guardian_name', 
                 'guardian_phone', 'guardian_email', 'emergency_contact', 'admission_date', 
                 'blood_group', 'medical_conditions', 'is_active']
    
    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
            if hasattr(user, 'student_profile'):
                raise serializers.ValidationError("User already has a student profile")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        
        # Update user's profile role
        profile = user.profile
        profile.role = 'student'
        profile.save()
        
        return Student.objects.create(user=user, **validated_data) 