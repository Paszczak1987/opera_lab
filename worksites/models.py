from django.conf import settings
from django.db import models


class Worksite(models.Model):
    """Construction site definition shared between clients and laboratories."""

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    office_address = models.CharField(max_length=255)
    clients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='worksites',
        blank=True,
        limit_choices_to={'role': 'client'},
        help_text='Clients allowed to manage and submit orders for this worksite.',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'

# Create your models here.
