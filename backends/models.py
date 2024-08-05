from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('accountant', 'Accountant'),
        ('director', 'Director'),
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES)
    school = models.ForeignKey('School', on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class School(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

class Classroom(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

class Subject(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

class Enrollment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

class Exam(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='ExamSubject')

class ExamSubject(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class StudentGrade(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.FloatField()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    matricule = models.CharField(max_length=20, unique=True)  # Unique identifier for students
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=15, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)
    parent_address = models.CharField(max_length=255, blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone_number = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_address = models.CharField(max_length=255, blank=True, null=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    matricule = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    hire_date = models.DateField()
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    documents = models.FileField(upload_to='teacher_documents/', blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
