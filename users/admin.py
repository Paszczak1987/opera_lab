from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role i laboratoria", {"fields": ("role", "active_laboratory", "country_code", "country_name")}),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "country_code",
        "active_laboratory",
        "is_active",
    )
    list_filter = ("role", "is_active", "country_code")
    readonly_fields = ("country_name",)
