# main/views.py
import zipfile
import os
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch, Q
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.models import Group
from .forms import *
from .models import *


#Done
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            role = form.cleaned_data.get('role')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


#Done
def user_login(request):
    if request.method == 'POST':
        form =  CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'main/login.html', {'form': form})


#Done
@login_required
def update_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('update_profile', user_id=user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = UserProfileForm(instance=user)

    return render(request, 'main/update_profile.html', {
        'form': profile_form, 'profile_menu_active': 'active'
    })

#Done
@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'main/view_profile.html', {'user': user})

#Done
@login_required
def update_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        password_form = UserPasswordChangeForm(user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated.')
            return redirect('update_password', user_id=user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = UserPasswordChangeForm(user)

    return render(request, 'main/update_password.html', {
        'form': password_form, 'profile_menu_active': 'active'
    })

#Done
@login_required
def create_course(request):
    if request.method == 'POST' and request.user.role.name == 'teacher':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)  # Do not commit yet, we'll set the teacher
            course.teacher = request.user     # Set the teacher to the current user
            course.image = request.FILES.get('image')  # Handle the image file
            course.save()  # Save the course instance
            return redirect('home')
    else:
        form = CourseCreationForm()
    return render(request, 'main/create_course.html', {'form': form, 'course_menu_active': 'active'})


#Done
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the logged-in user is the teacher of the course
    if request.user != course.teacher:
        return redirect('home')  # Or return a permission denied page

    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()  # Save the updated course
            return redirect('home')  # Redirect to the home page or course detail page
    else:
        form = CourseCreationForm(instance=course)

    return render(request, 'main/edit_course.html', {'form': form, 'course': course, 'course_menu_active': 'active'})


#Done
@login_required
def list_course(request):
    user = request.user
    query_param = request.GET.get('q').strip() if request.GET.get('q') else None
    
    
    courses = Course.objects.all()
    
    if query_param:
        courses = courses.filter(name__icontains=query_param)

    course_list = []
    for course in courses:
        # Fetch enrollments for the course
        enrollments = CourseEnrollment.objects.filter(course=course).select_related('student')
        
        # Check if the current user is enrolled in this course
        is_enrolled = enrollments.filter(student=user).exists()

        course_list.append({
            'course': course,
            'is_enrolled': is_enrolled,
            'enrollments': enrollments,   # Add enrollments if you need to display them
        })

    return render(request, 'main/list_course.html', {'courses': course_list, 
            'course_menu_active': 'active'})

@login_required
def view_students(request):
    user = request.user
    query_param = request.GET.get('q').strip() if request.GET.get('q') else None

    students = User.objects.filter(role__name='student')

    if query_param:
        students = students.filter(Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param))

    student_list = []
    for student in students:
        # Fetch enrollments for the student
        enrollments = CourseEnrollment.objects.filter(student=student).select_related('course')
        
        student_list.append({
            'student': student,
            'enrollments': enrollments,  # Add enrollments if you need to display them
        })

    return render(request, 'main/view_students.html', {'students': student_list, 
            'student_menu_active': 'active'})

# Done
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_teachers(request):
    user = request.user
    query_param = request.GET.get('q').strip() if request.GET.get('q') else None

    teachers = User.objects.filter(role__name='teacher')

    if query_param:
        teachers = teachers.filter(Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param))

    teacher_list = []
    for teacher in teachers:
        # Fetch courses taught by the teacher
        courses = Course.objects.filter(teacher=teacher)
        
        teacher_list.append({
            'teacher': teacher,
            'courses': courses,  # Add courses if you need to display them
        })

    return render(request, 'main/view_teachers.html', {'teachers': teacher_list, 
            'teacher_menu_active': 'active'})

# Done
@login_required
def join_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    if user.role.name == 'teacher':
        return redirect('home')
    
    # Check if the user is already enrolled
    enrollment, created = CourseEnrollment.objects.get_or_create(course=course, student=request.user)
    
    if created:
        
        # Notify the teacher about the new enrollment
        Notification.objects.create(
            user=course.teacher,
            course=course,
            message=f'Student {user.username} has enrolled in your course "{course.name}".'
        )

        
    return redirect('home')


# Done
@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.file = request.FILES.get('file') 
            material.save()
            
            # Notify all students enrolled in the course
            enrolled_students = CourseEnrollment.objects.filter(course=course).select_related('student')
            for enrollment in enrolled_students:
                Notification.objects.create(
                    user=enrollment.student,
                    course=course,
                    message=f'New material "{material.name}" has been added to the course "{course.name}".'
                )
            return redirect('view_course_detail', course_id=course.id)
    
    return redirect('view_course_detail', course_id=course.id)
   
    
# Done
@login_required
@login_required
def view_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    
    # Fetch course materials and enrolled students
    course_materials = CourseMaterial.objects.filter(course=course)
    joined_students = course.enrollments.all().select_related('student')
    
    # Check if the user is enrolled and if they are blocked
    course_enroll = CourseEnrollment.objects.filter(course=course, student=user).first()
    is_student_joined = course_enroll is not None
    is_student_blocked = course_enroll.is_blocked if is_student_joined else False
    is_teacher_owner = True if user.role.name == 'teacher' and course.teacher == user else False
    has_comments_permission = (user.role.name == 'teacher' and is_teacher_owner) or (user.role.name == 'student' and is_student_joined and not is_student_blocked)
    
    # Fetch comments related to the course
    comments = Comment.objects.filter(course=course).select_related('user').order_by('-created_at')
    
    # Handle status update form submission
    if request.method == 'POST' and 'status' in request.POST:
        status = request.POST.get('status')
        if is_student_joined:
            course_enroll.status = status
            course_enroll.save()
            messages.success(request, 'Your course status has been updated.')
        return redirect('view_course_detail', course_id=course.id)

    context = { 
        'is_teacher_owner': is_teacher_owner,
        'is_student_joined': is_student_joined, 
        'is_student_blocked': is_student_blocked,
        'has_comments_permission': has_comments_permission,
        'course': course,
        'course_menu_active': 'active', 
        'joined_students': joined_students,
        'course_materials': course_materials,
        'comments': comments,
        'course_enroll': course_enroll,
    }
    return render(request, 'main/view_course_detail.html', context)


# Done
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(reverse('view_course_detail', args=[notification.course.id]))

# Done
@login_required
def download_all_materials(request, course_id):
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


# Done
@login_required
def block_student(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(CourseEnrollment, course=course, student_id=student_id)
    
    enrollment.is_blocked = True
    enrollment.save()

    return redirect('view_course_detail', course_id=course.id)

# Done
@login_required
def unblock_student(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(CourseEnrollment, course=course, student_id=student_id)
    
    enrollment.is_blocked = False
    enrollment.save()

    return redirect('view_course_detail', course_id=course.id)


# Done
@login_required
def home(request):
    user = request.user
    query_param = request.GET.get('q').strip() if request.GET.get('q') else None
    
    if user.role.name == 'teacher':
        courses = Course.objects.filter(teacher=user)
    else:
        courses = Course.objects.filter(enrollments__student=user, enrollments__mode='Active').distinct()
        print(courses )
    
    if query_param:
        courses = courses.filter(name__icontains=query_param)

    course_list = []
    for course in courses:
        # Fetch enrollments for the course
        enrollments = CourseEnrollment.objects.filter(course=course).select_related('student')
        
        # Check if the current user is enrolled in this course
        is_enrolled = enrollments.filter(student=user).exists()

        course_list.append({
            'course': course,
            'is_enrolled': is_enrolled,
            'enrollments': enrollments,   # Add enrollments if you need to display them
        })

    return render(request, 'main/home.html', {'courses': course_list, 
            'home_menu_active': 'active',})


# Done
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    course_name = course.name
    course.delete()
    messages.success(request, f'Course "{course_name}" has been deleted successfully.')
    return redirect('home')  # Redirect to the course list page or another page

