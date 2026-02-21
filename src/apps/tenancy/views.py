from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tenancy.models import Client
from apps.tenancy.serializers import TenantSerializer, TenantSwitchSerializer
from apps.tenancy.services import switch_tenant_isolation


class TenantCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAdminUser]


class TenantSwitchIsolationView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, tenant_uuid):
        tenant = generics.get_object_or_404(Client, tenant_uuid=tenant_uuid)
        serializer = TenantSwitchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        switch_tenant_isolation(tenant, serializer.validated_data["isolation_mode"])
        return Response({"detail": "Tenant isolation updated"}, status=status.HTTP_200_OK)
