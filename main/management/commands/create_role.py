# main/management/commands/create_roles.py

from django.core.management.base import BaseCommand
from main.models import Role

class Command(BaseCommand):
    help = 'Create default roles'

    def handle(self, *args, **kwargs):
        roles = ['teacher', 'student', 'Owner']
        for role in roles:
            group, created = Role.objects.get_or_create(name=role,)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created role: {role}'))
            else:
                self.stdout.write(self.style.WARNING(f'Role {role} already exists'))