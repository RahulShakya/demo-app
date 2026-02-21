from django.db import models

from apps.tenancy.models import TenantAwareModel


class Project(TenantAwareModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("tenant", "name")

    def __str__(self) -> str:
        return self.name
