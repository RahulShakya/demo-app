from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    tenant = models.ForeignKey("tenancy.Client", null=True, blank=True, on_delete=models.SET_NULL, related_name="users")
