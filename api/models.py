from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Profile(models.Model):
    """Profile model to extend User with role information"""
    ROLE_CHOICES = settings.USER_ROLES
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
    
    class Meta:
        db_table = 'profiles'


class Subject(models.Model):
    """Subject model for academic subjects"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        db_table = 'subjects'
        ordering = ['name']


class Teacher(models.Model):
    """Teacher model extending User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    class Meta:
        db_table = 'teachers'
        ordering = ['user__first_name', 'user__last_name']


class Class(models.Model):
    """Class model for academic classes"""
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    academic_year = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes')
    subjects = models.ManyToManyField(Subject, related_name='classes')
    room_number = models.CharField(max_length=20, blank=True, null=True)
    max_students = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.grade_level}{self.section} ({self.academic_year})"
    
    class Meta:
        db_table = 'classes'
        ordering = ['grade_level', 'section']
        unique_together = ['grade_level', 'section', 'academic_year']


class Student(models.Model):
    """Student model extending User"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20)
    class_enrolled = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='students')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    guardian_name = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=15)
    guardian_email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15)
    admission_date = models.DateField()
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
    
    class Meta:
        db_table = 'students'
        ordering = ['user__first_name', 'user__last_name']
        unique_together = ['roll_number', 'class_enrolled']


class Assignment(models.Model):
    """Assignment model for academic assignments"""
    ASSIGNMENT_TYPES = [
        ('homework', 'Homework'),
        ('project', 'Project'),
        ('quiz', 'Quiz'),
        ('test', 'Test'),
        ('exam', 'Exam'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES, default='homework')
    total_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    instructions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.class_assigned})"
    
    class Meta:
        db_table = 'assignments'
        ordering = ['-due_date']


class Grade(models.Model):
    """Grade model for student grades"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    grade_letter = models.CharField(max_length=2, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    graded_date = models.DateTimeField(auto_now_add=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='graded_assignments')
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}: {self.marks_obtained}/{self.assignment.total_marks}"
    
    def calculate_percentage(self):
        return (self.marks_obtained / self.assignment.total_marks) * 100
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade letter based on percentage
        percentage = self.calculate_percentage()
        if percentage >= 90:
            self.grade_letter = 'A+'
        elif percentage >= 80:
            self.grade_letter = 'A'
        elif percentage >= 70:
            self.grade_letter = 'B+'
        elif percentage >= 60:
            self.grade_letter = 'B'
        elif percentage >= 50:
            self.grade_letter = 'C+'
        elif percentage >= 40:
            self.grade_letter = 'C'
        else:
            self.grade_letter = 'F'
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'grades'
        unique_together = ['student', 'assignment']
        ordering = ['-graded_date']


class Attendance(models.Model):
    """Attendance model for daily attendance"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='marked_attendance')
    notes = models.TextField(blank=True, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} - {self.get_status_display()}"
    
    class Meta:
        db_table = 'attendance'
        unique_together = ['student', 'class_attended', 'subject', 'date']
        ordering = ['-date', 'student__user__first_name']


# Signal to create Profile when User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='student')  # Default role

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
