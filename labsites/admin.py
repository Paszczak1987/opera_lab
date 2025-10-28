from django.contrib import admin

from .forms import LabSiteAdminForm
from .models import LabSite


@admin.register(LabSite)
class LabSiteAdmin(admin.ModelAdmin):
    form = LabSiteAdminForm
    list_display = ("name", "code", "short_name")
    list_filter = ("managers",)
    search_fields = ("name", "short_name", "code")
    ordering = ("name",)
    filter_horizontal = ("technicians", "managers")
    fieldsets = (
        ("Informacje podstawowe", {"fields": ("name", "short_name", "code", "address")}),
        (
            "Personel",
            {
                "fields": ("technicians", "managers"),
                "description": "Przypisz technikow i kierownikow pracujacych w laboratorium.",
            },
        ),
    )
