from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Uzytkownik musi miec nazwe uzytkownika.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")  # automatyczna rola dla superusera

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("client", "Client"),
        ("manager", "Manager"),
        ("technician", "Technician"),
        ("viewer", "Viewer"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    active_laboratory = models.ForeignKey(
        "labsites.LabSite",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="active_managers",
        help_text="Ostatnio wybrane aktywne laboratorium kierownika.",
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
