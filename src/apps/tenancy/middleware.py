from django.http import JsonResponse

from apps.tenancy.context import clear_current_tenant, set_current_tenant
from apps.tenancy.models import Client, IsolationMode


class HybridTenantMiddleware:
    header_name = "HTTP_X_TENANT_ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = getattr(request, "tenant", None)

        if tenant and getattr(tenant, "isolation_mode", None) in {IsolationMode.SCHEMA, IsolationMode.DEDICATED_DB}:
            set_current_tenant(tenant)
            response = self.get_response(request)
            clear_current_tenant()
            return response

        tenant_id = request.META.get(self.header_name)
        if request.path.startswith("/api/") and tenant_id:
            try:
                shared_tenant = Client.objects.get(tenant_uuid=tenant_id)
                request.tenant = shared_tenant
                set_current_tenant(shared_tenant)
            except Client.DoesNotExist:
                return JsonResponse({"detail": "Invalid X-Tenant-ID"}, status=400)

        response = self.get_response(request)
        clear_current_tenant()
        return response
