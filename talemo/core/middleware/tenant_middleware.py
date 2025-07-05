"""
Tenant middleware for multi-tenant functionality.
"""
from django.conf import settings
from django.db import connection
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware for handling multi-tenant functionality.
    """
    def process_request(self, request):
        """
        Process the request and set the tenant.
        """
        print("TenantMiddleware.process_request called")
        # Get the hostname from the request
        hostname = request.get_host().split(':')[0]
        print(f"Resolving tenant for hostname: {hostname}")

        # Check if we're using a custom header for tenant identification (useful for API requests)
        tenant_id = request.headers.get('X-Tenant-ID')

        # If we have a tenant ID in the header, use it
        if tenant_id:
            try:
                from talemo.core.models import Tenant
                tenant = Tenant.objects.get(schema_name=tenant_id)
                connection.set_tenant(tenant)
                if tenant.schema_name == 'public':
                    request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                    print(f"Using public schema urlconf: {settings.PUBLIC_SCHEMA_URLCONF}")
                return None
            except Tenant.DoesNotExist:
                raise Http404("Tenant does not exist")

        # Otherwise, use the hostname to identify the tenant
        try:
            from talemo.core.models import Domain
            domain = Domain.objects.get(domain=hostname)
            connection.set_tenant(domain.tenant)
            if domain.tenant.schema_name == 'public':
                request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                print(f"Using public schema urlconf: {settings.PUBLIC_SCHEMA_URLCONF}")
            return None
        except Domain.DoesNotExist:
            # If we're in development, try to find any domain for the public tenant
            if settings.DEBUG:
                from talemo.core.models import Tenant, Domain
                try:
                    # Try to get the public tenant
                    tenant = Tenant.objects.get(schema_name='public')

                    # Check if we have any domains for this tenant
                    domains = Domain.objects.filter(tenant=tenant)
                    if domains.exists():
                        # Create a new domain for the current hostname if it doesn't exist
                        if not Domain.objects.filter(domain=hostname).exists():
                            Domain.objects.create(
                                domain=hostname,
                                tenant=tenant,
                                is_primary=False
                            )
                            print(f"Created new domain record for {hostname}")

                    connection.set_tenant(tenant)
                    request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                    print(f"Using public schema urlconf: {settings.PUBLIC_SCHEMA_URLCONF}")
                    return None
                except Tenant.DoesNotExist:
                    # If no public tenant exists, create one
                    from django.contrib.auth.models import User
                    admin_user = User.objects.filter(is_superuser=True).first()
                    if admin_user:
                        tenant = Tenant.objects.create(
                            name='Public',
                            schema_name='public',
                            owner=admin_user
                        )
                        # Create a domain for the current hostname
                        Domain.objects.create(
                            domain=hostname,
                            tenant=tenant,
                            is_primary=True
                        )
                        print(f"Created new tenant and domain record for {hostname}")
                        connection.set_tenant(tenant)
                        request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                        print(f"Using public schema urlconf: {settings.PUBLIC_SCHEMA_URLCONF}")
                        return None

            # If we're not in development or couldn't find/create a default tenant, raise 404
            raise Http404("Tenant does not exist")
