from django.db import transaction

from apps.tenancy.models import Client, IsolationMode


@transaction.atomic
def switch_tenant_isolation(tenant: Client, target_mode: str) -> Client:
    if tenant.isolation_mode == target_mode:
        return tenant

    if target_mode == IsolationMode.SCHEMA and tenant.schema_name == "public":
        tenant.schema_name = f"tenant_{tenant.slug}"
        tenant.save()
        tenant.create_schema(check_if_exists=True)
    tenant.isolation_mode = target_mode
    tenant.save(update_fields=["isolation_mode", "schema_name"])
    return tenant
