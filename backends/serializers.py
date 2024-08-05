from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, School, Classroom, Subject, Enrollment, Exam, ExamSubject, StudentGrade
from .utils import generate_matricule

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = 'CustomUserSerializer'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('uid', 'name', 'address')

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('uid', 'name', 'school')

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('uid', 'name', 'school')

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('uid', 'student', 'classroom', 'date_enrolled')

class ExamSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubject
        fields = ('uid', 'exam', 'subject')

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('uid', 'name', 'date', 'classroom', 'subjects')

class StudentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGrade
        fields = ('uid', 'enrollment', 'exam', 'subject', 'grade')

class StudentGradeBulkSerializer(serializers.Serializer):
    grades = serializers.ListField(
        child=serializers.DictField()
    )

    def validate_grades(self, value):
        required_fields = {'enrollment', 'exam', 'subject', 'grade'}
        for item in value:
            if not required_fields.issubset(item.keys()):
                raise serializers.ValidationError("Chaque entrée doit contenir les champs : 'enrollment', 'exam', 'subject', 'grade'.")
            if not isinstance(item.get('grade'), (int, float)):
                raise serializers.ValidationError("Le champ 'grade' doit être un nombre.")
        return value

    def create(self, validated_data):
        grades_data = validated_data.get('grades')
        student_grades = []
        for grade_data in grades_data:
            enrollment = grade_data.get('enrollment')
            exam = grade_data.get('exam')
            subject = grade_data.get('subject')
            grade = grade_data.get('grade')

            student_grade = StudentGrade.objects.create(
                enrollment=enrollment,
                exam=exam,
                subject=subject,
                grade=grade
            )
            student_grades.append(student_grade)
        return student_grades

class StudentSerializer(serializers.ModelSerializer):
    matricule = serializers.CharField(read_only=True)  # Make matricule read-only

    class Meta:
        model = Student
        fields = ( 'user', 'first_name', 'last_name', 'matricule', 'date_of_birth', 'phone_number', 'address',
                  'blood_group', 'allergies', 'parent_name', 'parent_phone_number', 'parent_email', 'parent_address',
                  'guardian_name', 'guardian_phone_number', 'guardian_email', 'guardian_address')

    def create(self, validated_data):
        # Generate matricule before creating the Student
        matricule = generate_matricule('student')  # Assuming 'student' is the type of matricule
        validated_data['matricule'] = matricule
        student = super().create(validated_data)
        return student

    def update(self, instance, validated_data):
        # Optionally handle update logic for matricule if needed
        return super().update(instance, validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    matricule = serializers.CharField(read_only=True)  # Make matricule read-only

    class Meta:
        model = Teacher
        fields = ( 'user', 'matricule', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address',
                  'qualifications', 'hire_date', 'photo', 'documents', 'salary')

    def create(self, validated_data):
        # Generate matricule before creating the Teacher
        matricule = generate_matricule('teacher')  # Assuming 'teacher' is the type of matricule
        validated_data['matricule'] = matricule
        teacher = super().create(validated_data)
        return teacher

    def update(self, instance, validated_data):
        # Optionally handle update logic for matricule if needed
        return super().update(instance, validated_data)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'email', 'password', 'password2', 'role', 'school', 'photo', 'uid')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            school=validated_data.get('school'),
            photo=validated_data.get('photo')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'school', 'photo', 'uid')

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "Les mots de passe ne correspondent pas"})
        return data

class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
