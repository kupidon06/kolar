from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models import User,Student, Teacher, School, Classroom, Subject, Enrollment, Exam, ExamSubject, StudentGrade
from .serializers import (
    UserSerializer, SchoolSerializer, ClassroomSerializer, SubjectSerializer, EnrollmentSerializer,
    ExamSerializer, ExamSubjectSerializer, StudentGradeSerializer, StudentGradeBulkSerializer,
    StudentSerializer, TeacherSerializer, UserCreateSerializer, UserUpdateSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer, ActivationSerializer
)

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.AllowAny]

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamSubjectViewSet(viewsets.ModelViewSet):
    queryset = ExamSubject.objects.all()
    serializer_class = ExamSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentGradeViewSet(viewsets.ModelViewSet):
    queryset = StudentGrade.objects.all()
    serializer_class = StudentGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        serializer = StudentGradeBulkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'grades created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

### User Management Views

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.role == 'student':
            queryset = User.objects.filter(id=user.id)
        elif user.role == 'teacher':
            queryset = User.objects.filter(id=user.id)
        elif user.role == 'director':
            queryset = User.objects.filter(school=user.school)
        elif user.role == 'accountant':
            queryset = User.objects.filter(school=user.school)
        else:
            queryset = User.objects.none()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'user created', 'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = get_user_model().objects.get(pk=pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'user updated', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_user_model().objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Custom Password Reset and Confirmation Views

class CustomPasswordResetViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # Allow anyone to request a password reset

    def create(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # Implement custom password reset logic if needed
            return Response({'status': 'password reset email sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordResetConfirmViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # Allow anyone to confirm a password reset

    def create(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # Implement custom password reset confirmation logic if needed
            return Response({'status': 'password has been reset'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
