# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import *

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'First Name'}),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Last Name'}),
        label="Last Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Email'}),
        label="Email"
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control form-control-prepended'}),
        label="Gender"
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(name__in=['teacher', 'student']),
        empty_label="Select Role",
        widget=forms.Select(attrs={'class': 'form-control form-control-prepended'}),
        label="Role"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-prepended'}),
        label="Profile Photo",
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'role', 'password1', 'password2', 'photo',]


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Course Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
  
class CourseMaterialForm(forms.ModelForm):
    
    class Meta:
        model = CourseMaterial
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'File Name'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'Password'}),
        label="Password"
    )

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-prepended'}))
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        widget=forms.Select(attrs={'class': 'form-control form-control-prepended'}),
        label="Gender"
    )
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-prepended'}))

    about_me = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-prepended', 'placeholder': 'About Me'}),
        required=False,
        label="About Me"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'photo', 'status', 'about_me']
        

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}))
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']   
    