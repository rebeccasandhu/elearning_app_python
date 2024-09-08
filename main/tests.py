from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from .models import Course, CourseEnrollment, Comment, Notification, Role
from .forms import UserRegistrationForm, UserProfileForm, UserPasswordChangeForm

User = get_user_model()
def generate_test_image():
        # Create an image in memory
        img = Image.new('RGB', (100, 100), color = (73, 109, 137))
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io
    
class UserModelTest(TestCase):
    def setUp(self):
        # Create necessary roles
        self.teacher_role = Role.objects.create(name='teacher', description='Teacher Role')
        self.student_role = Role.objects.create(name='student', description='Student Role')

        # Create a user with a teacher role
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            gender="Male",
            role=self.teacher_role
        )

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john@example.com")
        self.assertTrue(self.user.check_password("password123"))

    def test_user_str(self):
        self.assertEqual(str(self.user), f"{self.user.email} - {self.user.role}")

class CourseModelTest(TestCase):
    def setUp(self):
        self.teacher_role = Role.objects.create(name='teacher', description='Teacher Role')
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            gender="Male",
            role=self.teacher_role
        )
        self.course = Course.objects.create(
            name="Python Basics",
            description="Learn the basics of Python.",
            teacher=self.user
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, "Python Basics")
        self.assertEqual(self.course.description, "Learn the basics of Python.")
        self.assertEqual(self.course.teacher, self.user)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Python Basics - John Doe")

class CourseEnrollmentModelTest(TestCase):
    def setUp(self):
        self.teacher_role = Role.objects.create(name='teacher', description='Teacher Role')
        self.student_role = Role.objects.create(name='student', description='Student Role')
        
        self.student = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            password="password123",
            gender="Female",
            role=self.student_role
        )
        self.course = Course.objects.create(
            name="Django Basics",
            description="Learn the basics of Django.",
            teacher=self.student  # This should typically be another user
        )
        self.enrollment = CourseEnrollment.objects.create(
            course=self.course,
            student=self.student,
            status="Inprogress"
        )

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.status, "Inprogress")

    def test_enrollment_str(self):
        self.assertEqual(str(self.enrollment), "jane@example.com enrolled in Django Basics with status Inprogress")

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_role = Role.objects.create(name='teacher', description='Teacher Role')
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            gender="Male",
            role=self.teacher_role
        )
        self.client.login(username='john@example.com', password='password123')
        self.course = Course.objects.create(
            name="Python Basics",
            description="Learn the basics of Python.",
            teacher=self.user
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_course_detail_view(self):
        response = self.client.get(reverse('view_course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/view_course_detail.html')

    def test_course_creation_view(self):
        response = self.client.get(reverse('create_course'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_course.html')

class FormsTest(TestCase):
    def setUp(self):
        self.teacher_role = Role.objects.create(name='teacher', description='Teacher Role')
    
    def test_user_registration_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'gender': 'Male',
            'role': self.teacher_role.id,  
            'password1': 'AsecureP@ssword1',
            'password2': 'AsecureP@ssword1',
        }
        form = UserRegistrationForm(data=form_data)
        if not form.is_valid():
            print("UserRegistrationForm errors:", form.errors)  # Print form errors for debugging
        self.assertTrue(form.is_valid())


    def test_user_profile_form(self):
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            gender="Male",
            role=self.teacher_role
        )
        form_data = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'email': 'johnny@example.com',
            'gender': 'Male',
            'role': self.teacher_role.id,  # Add role to the form data
        }
        # Create a valid image file
        image_file = SimpleUploadedFile(name='test_image.jpg', content=generate_test_image().read(), content_type='image/jpeg')

        form = UserProfileForm(data=form_data, files={'photo': image_file}, instance=user)
        if not form.is_valid():
            print("UserProfileForm errors:", form.errors)  # Print form errors for debugging
        self.assertTrue(form.is_valid())
        
    def test_password_change_form(self):
        user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            gender="Male",
            role=self.teacher_role
        )
        form_data = {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        form = UserPasswordChangeForm(user=user, data=form_data)
        self.assertTrue(form.is_valid())