# Generated by Django 5.0.4 on 2024-08-31 13:45

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('first_name', models.CharField(help_text='First name', max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(help_text='Last name', max_length=255, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], help_text='Gender', max_length=30, verbose_name='Gender')),
                ('email', models.EmailField(help_text='Email Address', max_length=250, unique=True, verbose_name='Email Address')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('status', models.CharField(blank=True, help_text='Status (for students only)', max_length=255, null=True, verbose_name='Status')),
                ('about_me', models.TextField(blank=True, help_text='About me', null=True, verbose_name='About me')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Users',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.FileField(blank=True, null=True, upload_to='course_images/')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.course')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('status', models.CharField(choices=[('Inprogress', 'Inprogress'), ('Completed', 'Completed'), ('Yet to start', 'Yet to start')], default='Yet to start', help_text='Status', max_length=30, verbose_name='Status')),
                ('is_blocked', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='main.course')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='course_materials/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='main.course')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='main.course')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Data created on', verbose_name='Created on')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Data modified on', verbose_name='Modified by')),
                ('mode', models.CharField(choices=[('Active', 'Active'), ('Deactivated', 'Deactivated'), ('Trash', 'Trash')], default='Active', max_length=30, verbose_name='Mode')),
                ('name', models.CharField(help_text='User role name', max_length=50, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, help_text='User role description', verbose_name='Description')),
                ('created_by', models.ForeignKey(editable=False, help_text='Data created by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('modified_by', models.ForeignKey(editable=False, help_text='Data modified by', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Modified by')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'role',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, help_text='Role', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='main.role', verbose_name='Role'),
        ),
    ]
