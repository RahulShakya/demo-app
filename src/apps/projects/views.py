from rest_framework import permissions, viewsets

from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer
from apps.tenancy.models import IsolationMode


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tenant = getattr(self.request, "tenant", None) or getattr(self.request.user, "tenant", None)
        queryset = Project.objects.all()
        if tenant is None:
            return queryset.none()
        if tenant.isolation_mode == IsolationMode.SHARED:
            return queryset.filter(tenant=tenant)
        return queryset

    def perform_create(self, serializer):
        tenant = getattr(self.request, "tenant", None) or getattr(self.request.user, "tenant", None)
        serializer.save(tenant=tenant)
