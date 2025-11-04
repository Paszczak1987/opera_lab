from django.contrib import admin

from .models import Worksite


@admin.register(Worksite)
class WorksiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'office_address', 'country_code')
    search_fields = ('name', 'short_name', 'code', 'office_address', 'country_name')
    list_filter = ('country_code',)
    readonly_fields = ('country_name',)
    fields = ('name', 'short_name', 'code', 'office_address', 'country_code', 'country_name', 'clients')
    filter_horizontal = ('clients',)

# Register your models here.
