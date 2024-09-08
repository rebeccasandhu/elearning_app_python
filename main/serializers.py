# main/serializers.py

from rest_framework import serializers
from .models import User, Course, CourseMaterial, Comment, CourseEnrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'role', 'photo', 'status', 'about_me']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'role', 'password', 'password_confirm', 'photo']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'photo', 'status', 'about_me']

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['name', 'file']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'image', 'teacher']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user']

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'student', 'status', 'is_blocked', 'created_on']

class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    materials = CourseMaterialSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    enrollments = CourseEnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'image', 'teacher', 'materials', 'comments', 'enrollments']