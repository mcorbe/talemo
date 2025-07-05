"""
Management command to seed the database with initial data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from talemo.core.models import Tenant, Domain, Profile
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('--domain', type=str, default='localhost', help='Domain for the public tenant')
        parser.add_argument('--admin-username', type=str, default='admin', help='Username for the admin user')
        parser.add_argument('--admin-password', type=str, default='admin', help='Password for the admin user')
        parser.add_argument('--admin-email', type=str, default='admin@example.com', help='Email for the admin user')
        parser.add_argument('--create-test-users', action='store_true', help='Create test users')
        parser.add_argument('--test-users-count', type=int, default=3, help='Number of test users to create')

    def handle(self, *args, **options):
        domain_name = options['domain']
        admin_username = options['admin_username']
        admin_password = options['admin_password']
        admin_email = options['admin_email']
        create_test_users = options['create_test_users']
        test_users_count = options['test_users_count']

        # Ensure public tenant exists
        self._ensure_public_tenant(domain_name, admin_username, admin_password, admin_email)

        # Create profile for admin user if it doesn't exist
        admin_user = User.objects.get(username=admin_username)
        self._ensure_profile(admin_user)

        # Create test users if requested
        if create_test_users:
            self._create_test_users(test_users_count)

        # Initialize MinIO bucket if using MinIO
        if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME') and settings.AWS_STORAGE_BUCKET_NAME:
            self._initialize_minio()

        self.stdout.write(self.style.SUCCESS('Database seeding complete'))

    def _ensure_public_tenant(self, domain_name, username, password, email):
        """Ensure the public tenant exists."""
        # Check if public tenant already exists
        if not Tenant.objects.filter(schema_name='public').exists():
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
        else:
            self.stdout.write(self.style.SUCCESS('Public tenant already exists'))
            # Ensure domain exists
            tenant = Tenant.objects.get(schema_name='public')
            if not Domain.objects.filter(domain=domain_name, tenant=tenant).exists():
                domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
                domain.save()
                self.stdout.write(self.style.SUCCESS(f'Created domain: {domain_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Domain {domain_name} already exists'))

    def _ensure_profile(self, user):
        """Ensure the user has a profile."""
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'bio': f'Admin user bio',
                'is_parent': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Profile for user {user.username} already exists'))

    def _create_test_users(self, count):
        """Create test users with profiles."""
        for i in range(1, count + 1):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = 'password'

            # Get or create user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_active': True
                }
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created test user: {username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Found existing test user: {username}'))

            # Use get_or_create instead of direct creation
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Test user {i} bio',
                    'is_parent': True
                }
            )
            if profile_created:
                self.stdout.write(self.style.SUCCESS(f'Created profile for test user: {username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Found existing profile for test user: {username}'))

    def _initialize_minio(self):
        """Initialize MinIO bucket if it doesn't exist."""
        try:
            import boto3
            from botocore.client import Config
            from botocore.exceptions import ClientError

            # Configure the MinIO client
            s3_client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4'),
                region_name='us-east-1'  # This is required but not used by MinIO
            )

            # Check if the bucket exists
            try:
                s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
                self.stdout.write(self.style.SUCCESS(f'MinIO bucket {settings.AWS_STORAGE_BUCKET_NAME} already exists'))
            except ClientError:
                # Create the bucket
                s3_client.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
                self.stdout.write(self.style.SUCCESS(f'Created MinIO bucket: {settings.AWS_STORAGE_BUCKET_NAME}'))

                # Set the bucket policy to allow public read access
                bucket_policy = {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Sid': 'PublicReadGetObject',
                            'Effect': 'Allow',
                            'Principal': '*',
                            'Action': ['s3:GetObject'],
                            'Resource': [f'arn:aws:s3:::{settings.AWS_STORAGE_BUCKET_NAME}/*']
                        }
                    ]
                }
                s3_client.put_bucket_policy(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Policy=str(bucket_policy).replace("'", '"')
                )
                self.stdout.write(self.style.SUCCESS(f'Set public read policy for bucket: {settings.AWS_STORAGE_BUCKET_NAME}'))

        except ImportError:
            self.stdout.write(self.style.WARNING('boto3 not installed, skipping MinIO initialization'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error initializing MinIO: {str(e)}'))
