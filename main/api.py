import zipfile
import os
from io import BytesIO
from django.http import HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from .models import *
from .serializers import *


# User Registration API
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile API
class UpdateProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Ensure the user can only update their own profile


# Course API
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


# Course Detail API
class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course = super().get_object()
        user = self.request.user

        # Check if the user is enrolled and if they are blocked
        course_enroll = CourseEnrollment.objects.filter(course=course, student=user).first()
        course.is_student_joined = course_enroll is not None
        course.is_student_blocked = course_enroll.is_blocked if course.is_student_joined else False
        course.is_teacher_owner = True if user.role.name == 'teacher' and course.teacher == user else False
        course.has_comments_permission = (user.role.name == 'teacher' and course.is_teacher_owner) or (user.role.name == 'student' and course.is_student_joined and not course.is_student_blocked)
        
        return course


# Join Course API
class JoinCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        if user.role.name == 'teacher':
            return Response({'detail': 'Teachers cannot join courses'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollment, created = CourseEnrollment.objects.get_or_create(course=course, student=user)
        
        if created:
            Notification.objects.create(
                user=course.teacher,
                course=course,
                message=f'Student {user.username} has enrolled in your course "{course.name}".'
            )
        return Response({'detail': 'Enrolled successfully'}, status=status.HTTP_200_OK)


# View Students API
class ViewStudentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_param = request.GET.get('q')
        students = User.objects.filter(role__name='student')

        if query_param:
            students = students.filter(Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param))

        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)


# View Teachers API
class ViewTeachersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_param = request.GET.get('q')
        teachers = User.objects.filter(role__name='teacher')

        if query_param:
            teachers = teachers.filter(Q(first_name__icontains=query_param) | Q(last_name__icontains(query_param)))

        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)


# Upload Course Material API
class UploadMaterialAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseMaterialSerializer(data=request.data)

        if serializer.is_valid():
            material = serializer.save(course=course)
            
            # Notify all students enrolled in the course
            enrolled_students = CourseEnrollment.objects.filter(course=course).select_related('student')
            for enrollment in enrolled_students:
                Notification.objects.create(
                    user=enrollment.student,
                    course=course,
                    message=f'New material "{material.name}" has been added to the course "{course.name}".'
                )
            return Response({'message': 'Material uploaded successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Block Student API
class BlockStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, student_id):
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        enrollment = get_object_or_404(CourseEnrollment, course=course, student_id=student_id)
        
        enrollment.is_blocked = True
        enrollment.save()

        return Response({'message': 'Student blocked successfully'}, status=status.HTTP_200_OK)


# Unblock Student API
class UnblockStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id, student_id):
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        enrollment = get_object_or_404(CourseEnrollment, course=course, student_id=student_id)
        
        enrollment.is_blocked = False
        enrollment.save()

        return Response({'message': 'Student unblocked successfully'}, status=status.HTTP_200_OK)


# Mark Notification as Read API
class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)


# Download All Materials API
class DownloadAllMaterialsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Create a BytesIO object to hold the ZIP file in memory
        zip_buffer = BytesIO()

        # Create a new ZIP file inside the BytesIO object
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # Iterate over all course materials
            for material in course.materials.all():
                # Add each file to the ZIP file
                file_path = material.file.path
                file_name = os.path.basename(file_path)
                zip_file.write(file_path, file_name)

        # Set the buffer position to the beginning
        zip_buffer.seek(0)

        # Send the ZIP file back as a response
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename="{course.name}_materials.zip"'

        return response