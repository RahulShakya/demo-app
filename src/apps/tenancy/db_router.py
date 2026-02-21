from apps.tenancy.context import get_current_tenant
from apps.tenancy.models import IsolationMode


class TenantDatabaseRouter:
    def db_for_read(self, model, **hints):
        return self._db_alias(model)

    def db_for_write(self, model, **hints):
        return self._db_alias(model)

    def _db_alias(self, model):
        tenant = get_current_tenant()
        if tenant and tenant.isolation_mode == IsolationMode.DEDICATED_DB:
            return "dedicated"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "dedicated":
            return app_label in {"projects", "accounts", "tenancy", "common"}
        return True
