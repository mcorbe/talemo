"""
Management command to initialize the public tenant and domain.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from talemo.core.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Initialize the public tenant and domain'

    def add_arguments(self, parser):
        parser.add_argument('--domain', type=str, default='localhost', help='Domain for the public tenant')
        parser.add_argument('--username', type=str, default='admin', help='Username for the admin user')
        parser.add_argument('--password', type=str, default='admin', help='Password for the admin user')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Email for the admin user')

    def handle(self, *args, **options):
        domain_name = options['domain']
        username = options['username']
        password = options['password']
        email = options['email']

        # Check if public tenant already exists
        if Tenant.objects.filter(schema_name='public').exists():
            self.stdout.write(self.style.SUCCESS('Public tenant already exists'))
            return

        # Create admin user if it doesn't exist
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
        else:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f'Using existing admin user: {username}'))

        # Create public tenant
        tenant = Tenant(schema_name='public', name='Public Tenant', owner=user)
        tenant.save()
        self.stdout.write(self.style.SUCCESS('Created public tenant'))

        # Create domain for public tenant
        domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
        domain.save()
        self.stdout.write(self.style.SUCCESS(f'Created domain: {domain_name}'))

        self.stdout.write(self.style.SUCCESS('Public tenant initialization complete'))