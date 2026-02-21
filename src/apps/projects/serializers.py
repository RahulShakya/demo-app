from rest_framework import serializers

from apps.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "tenant", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "tenant"]
