from django.conf import settings
from django.db import models

class LabSite(models.Model):
    """Laboratory definition with assigned technicians and managers."""

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)

    technicians = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="laboratories",
        blank=True,
        limit_choices_to={"role": "technician"},
        help_text="Technicians assigned to work in this laboratory.",
    )
    managers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="managed_laboratories",
        blank=True,
        limit_choices_to={"role": "manager"},
        help_text="Managers overseeing this laboratory.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
