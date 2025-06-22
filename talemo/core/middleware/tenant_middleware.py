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
        # Get the hostname from the request
        hostname = request.get_host().split(':')[0]
        
        # Check if we're using a custom header for tenant identification (useful for API requests)
        tenant_id = request.headers.get('X-Tenant-ID')
        
        # If we have a tenant ID in the header, use it
        if tenant_id:
            try:
                from talemo.core.models import Tenant
                tenant = Tenant.objects.get(schema_name=tenant_id)
                connection.set_tenant(tenant)
                return None
            except Tenant.DoesNotExist:
                raise Http404("Tenant does not exist")
        
        # Otherwise, use the hostname to identify the tenant
        try:
            from talemo.core.models import Domain
            domain = Domain.objects.get(domain=hostname)
            connection.set_tenant(domain.tenant)
            return None
        except Domain.DoesNotExist:
            # If we're in development, use the default tenant
            if settings.DEBUG:
                from talemo.core.models import Tenant
                try:
                    tenant = Tenant.objects.get(schema_name='public')
                    connection.set_tenant(tenant)
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
                        connection.set_tenant(tenant)
                        return None
            
            # If we're not in development or couldn't find/create a default tenant, raise 404
            raise Http404("Tenant does not exist")