from django.contrib import admin

from .models import Worksite


@admin.register(Worksite)
class WorksiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'code', 'office_address')
    search_fields = ('name', 'short_name', 'code', 'office_address')
    filter_horizontal = ('clients',)

# Register your models here.
