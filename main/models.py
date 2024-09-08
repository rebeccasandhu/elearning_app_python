# main/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

MODE = (
    ('Active', 'Active'),
    ('Deactivated', 'Deactivated'),
    ('Trash', 'Trash')
)
GENDER = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))

class BaseModel(models.Model):
    created_by = models.ForeignKey('main.User', verbose_name=_('Created by'), on_delete=models.SET_NULL, editable=False, related_name="created_%(app_label)s_%(class)s_set", null=True, help_text=_('Data created by'))
    modified_by = models.ForeignKey('main.User', verbose_name=_('Modified by'), on_delete=models.SET_NULL, editable=False, related_name="modified_%(app_label)s_%(class)s_set", null=True, help_text=_('Data modified by'))
    created_on = models.DateTimeField(verbose_name=_('Created on'), auto_now_add=True, help_text=_('Data created on'))
    modified_on = models.DateTimeField(verbose_name=_('Modified by'), auto_now=True, help_text=_('Data modified on'))
    mode = models.CharField(verbose_name=_('Mode'), max_length=30, default='Active', choices=MODE)

    class Meta:
        abstract = True

class Role(BaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, help_text=_('User role name'))
    description = models.TextField(verbose_name=_('Description'), blank=True, help_text=_('User role description'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ('name',)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email  # Generate a unique username
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        validated_data = kwargs
        if not validated_data['email']:
            raise ValueError(_('Users must have an email'))

        if not validated_data['password']:
            password = self.model.objects.make_random_password(length=14,
                                                               allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

        password = validated_data.pop('password')
        validated_data.pop('role')
        validated_data['username'] =validated_data['email']
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.role = Role.objects.get(name="Owner")
        user.save(using=self._db)
        return user

class User(BaseModel, AbstractUser):
    first_name = models.CharField(verbose_name=_('First Name'), max_length=255, null=False, blank=False, help_text=_('First name'))
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=255, blank=False, null=False, help_text=_('Last name'))
    gender = models.CharField(verbose_name=_('Gender'), max_length=30, blank=False, null=False, choices=GENDER, help_text=_('Gender'))
    email = models.EmailField(verbose_name=_('Email Address'), unique=True, max_length=250, help_text=_('Email Address'))
    role = models.ForeignKey(Role, verbose_name=_('Role'), related_name='users', blank=True, null=True, on_delete=models.SET_NULL, help_text=_('Role'))
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    status = models.CharField(verbose_name=_('Status'), max_length=255, blank=True, null=True, help_text=_('Status (for students only)'))
    about_me = models.TextField(verbose_name=_('About me'), blank=True, null=True, help_text=_('About me'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'role']
    objects = UserManager()
    
    def __str__(self):
        return f'{str(self.email)} - {self.role}'
    
    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)
        
    class Meta:
        db_table = 'user'
        verbose_name = _('Users')
        verbose_name_plural = _('Users')

class Course(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.FileField(upload_to='course_images/', blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return f'{str(self.name)} - {self.teacher.first_name} {self.teacher.last_name}'
    
class CourseMaterial(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} for {self.course.name}'
    
class CourseEnrollment(BaseModel):
    COURSE_STATUS = (('Inprogress', 'Inprogress'), ('Completed', 'Completed'), ('Yet to start', 'Yet to start'))
    status = models.CharField(verbose_name=_('Status'), max_length=30, blank=False, null=False, default='Yet to start',
                              choices=COURSE_STATUS, help_text=_('Status'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.student.username} enrolled in {self.course.name} with status {self.status}'
    
    
class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.course.name}'


class Comment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course.name}'

    class Meta:
        ordering = ['-created_at']