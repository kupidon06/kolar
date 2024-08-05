from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolViewSet, ClassroomViewSet, SubjectViewSet, EnrollmentViewSet,
    ExamViewSet, ExamSubjectViewSet, StudentGradeViewSet, StudentViewSet,
    TeacherViewSet, UserViewSet, CustomPasswordResetViewSet, CustomPasswordResetConfirmViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'exam-subjects', ExamSubjectViewSet)
router.register(r'student-grades', StudentGradeViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('password-reset/', CustomPasswordResetViewSet.as_view({'post': 'create'}), name='password-reset'),
    path('password-reset-confirm/', CustomPasswordResetConfirmViewSet.as_view({'post': 'create'}), name='password-reset-confirm'),
]

