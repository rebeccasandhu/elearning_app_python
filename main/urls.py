# main/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import (
    RegisterAPIView, UpdateProfileAPIView, CourseDetailAPIView, JoinCourseAPIView,
    ViewStudentsAPIView, ViewTeachersAPIView, UploadMaterialAPIView, BlockStudentAPIView,
    UnblockStudentAPIView, MarkNotificationAsReadAPIView, DownloadAllMaterialsAPIView, CourseViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # API routes
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/profile/', UpdateProfileAPIView.as_view(), name='api_update_profile'),
    path('api/courses/<int:course_id>/', CourseDetailAPIView.as_view(), name='api_course_detail'),
    path('api/courses/<int:course_id>/join/', JoinCourseAPIView.as_view(), name='api_join_course'),
    path('api/students/', ViewStudentsAPIView.as_view(), name='api_view_students'),
    path('api/teachers/', ViewTeachersAPIView.as_view(), name='api_view_teachers'),
    path('api/courses/<int:course_id>/materials/upload/', UploadMaterialAPIView.as_view(), name='api_upload_material'),
    path('api/courses/<int:course_id>/block/<int:student_id>/', BlockStudentAPIView.as_view(), name='api_block_student'),
    path('api/courses/<int:course_id>/unblock/<int:student_id>/', UnblockStudentAPIView.as_view(), name='api_unblock_student'),
    path('api/notifications/<int:notification_id>/mark-as-read/', MarkNotificationAsReadAPIView.as_view(), name='api_mark_notification_as_read'),
    path('api/courses/<int:course_id>/materials/download/', DownloadAllMaterialsAPIView.as_view(), name='api_download_all_materials'),

    # Existing routes
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_course/', views.create_course, name='create_course'),
    path('courses/', views.list_course, name='list_course'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/view/', views.view_course_detail, name='view_course_detail'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/join/', views.join_course, name='join_course'),
    path('course/<int:course_id>/upload/', views.upload_material, name='upload_material'),
    path('course/<int:course_id>/download-all-materials/', views.download_all_materials, name='download_all_materials'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('course/<int:course_id>/block_student/<int:student_id>/', views.block_student, name='block_student'),
    path('course/<int:course_id>/unblock_student/<int:student_id>/', views.unblock_student, name='unblock_student'),
    path('profile/<int:user_id>/update_profile/', views.update_profile, name='update_profile'),
    path('profile/<int:user_id>/update_password/', views.update_password, name='update_password'),
    path('students/', views.view_students, name='view_students'),
    path('teachers/', views.view_teachers, name='view_teachers'),
    path('profile/<int:user_id>/view/', views.view_profile, name='view_profile'),
    path('', views.home, name='home'),
]