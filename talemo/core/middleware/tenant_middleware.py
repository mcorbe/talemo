"""
Tenant middleware for shared schema multi-tenant functionality.
"""
from django.conf import settings
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware for handling shared schema multi-tenant functionality.
    Sets the current tenant on the request object.
    """
    def process_request(self, request):
        """
        Process the request and set the tenant on the request object.
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
                tenant = Tenant.objects.get(id=tenant_id)
                request.tenant = tenant
                return None
            except Tenant.DoesNotExist:
                raise Http404("Tenant does not exist")

        # Otherwise, use the hostname to identify the tenant
        try:
            from talemo.core.models import Domain
            domain = Domain.objects.get(domain=hostname)
            request.tenant = domain.tenant
            return None
        except Domain.DoesNotExist:
            # If we're in development, try to find any domain or create a default tenant
            if settings.DEBUG:
                from talemo.core.models import Tenant, Domain

                # Try to get a default tenant
                default_tenant = Tenant.objects.filter(name='Default').first()

                if not default_tenant:
                    # Create a default tenant if none exists
                    default_tenant = Tenant.objects.create(
                        name='Default',
                        type='family'
                    )
                    print(f"Created default tenant")

                # Create a domain for the current hostname if it doesn't exist
                if not Domain.objects.filter(domain=hostname).exists():
                    Domain.objects.create(
                        domain=hostname,
                        tenant=default_tenant,
                        is_primary=True
                    )
                    print(f"Created new domain record for {hostname}")

                request.tenant = default_tenant
                return None

            # If we're not in development or couldn't find/create a default tenant, raise 404
            raise Http404("Tenant does not exist")
