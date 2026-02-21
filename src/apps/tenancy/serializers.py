from rest_framework import serializers

from apps.tenancy.models import Client, Domain, IsolationMode


class TenantSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ["id", "name", "slug", "tenant_uuid", "schema_name", "isolation_mode", "domain"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        domain = validated_data.pop("domain")
        client = Client.objects.create(**validated_data)
        Domain.objects.create(tenant=client, domain=domain, is_primary=True)
        return client


class TenantSwitchSerializer(serializers.Serializer):
    isolation_mode = serializers.ChoiceField(choices=IsolationMode.choices)
