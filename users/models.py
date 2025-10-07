from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('viewer', 'Viewer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # ewentualnie: przypisanie do laboratorium dodamy później w modelu Laboratory

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
