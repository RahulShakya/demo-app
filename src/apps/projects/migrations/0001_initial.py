from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tenancy", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="projects", to="tenancy.client")),
            ],
            options={"unique_together": {("tenant", "name")}},
        ),
    ]
