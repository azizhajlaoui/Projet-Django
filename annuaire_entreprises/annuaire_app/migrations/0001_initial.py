# Generated by Django 5.1.7 on 2025-04-10 19:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Entreprise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=255)),
                ("secteur", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("telephone", models.CharField(max_length=15)),
                ("adresse", models.CharField(max_length=255)),
                ("site_web", models.URLField(blank=True, null=True)),
                ("date_creation", models.DateTimeField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
