from django.urls import path

from apps.tenancy.views import TenantCreateView, TenantSwitchIsolationView

urlpatterns = [
    path("tenants/", TenantCreateView.as_view(), name="tenant-create"),
    path("tenants/<uuid:tenant_uuid>/switch-isolation/", TenantSwitchIsolationView.as_view(), name="tenant-switch"),
]
