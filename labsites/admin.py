from django.contrib import admin

from .forms import LabSiteAdminForm
from .models import LabSite


@admin.register(LabSite)
class LabSiteAdmin(admin.ModelAdmin):
    form = LabSiteAdminForm
    list_display = ("name", "code", "short_name", "country_code")
    list_filter = ("managers", "country_code")
    search_fields = ("name", "short_name", "code", "country_name")
    ordering = ("name",)
    filter_horizontal = ("technicians", "managers")
    readonly_fields = ("country_name",)
    fieldsets = (
        ("Informacje podstawowe", {"fields": ("name", "short_name", "code", "address", "country_code", "country_name")}),
        (
            "Personel",
            {
                "fields": ("technicians", "managers"),
                "description": "Przypisz technikow i kierownikow pracujacych w laboratorium.",
            },
        ),
    )
