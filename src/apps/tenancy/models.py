from django.db import models
import uuid
from django_tenants.models import DomainMixin, TenantMixin

from apps.common.models import TimestampedModel


class IsolationMode(models.TextChoices):
    SHARED = "shared", "Shared Database"
    SCHEMA = "schema", "Dedicated Schema"
    DEDICATED_DB = "dedicated_db", "Dedicated Database"


class Client(TenantMixin, TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    tenant_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    isolation_mode = models.CharField(max_length=20, choices=IsolationMode.choices, default=IsolationMode.SHARED)
    auto_create_schema = True

    def __str__(self) -> str:
        return f"{self.name} ({self.isolation_mode})"


class Domain(DomainMixin, TimestampedModel):
    pass


class TenantAwareModel(TimestampedModel):
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="%(class)ss")

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["tenant"]) ]
