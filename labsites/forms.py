from django import forms

from users.models import User

from .models import LabSite


class LabSiteAdminForm(forms.ModelForm):
    """Custom form for managing laboratories in admin."""

    class Meta:
        model = LabSite
        fields = ["name", "short_name", "code", "address", "technicians", "managers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["technicians"].queryset = User.objects.filter(role="technician")
        self.fields["managers"].queryset = User.objects.filter(role="manager")
        for field in ("technicians", "managers"):
            self.fields[field].help_text = ""


class LabSiteForm(forms.ModelForm):
    """Form used in the dashboard for creating or editing laboratories."""

    class Meta:
        model = LabSite
        fields = ["name", "short_name", "code", "address", "technicians", "managers"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Pelna nazwa laboratorium"}),
            "short_name": forms.TextInput(attrs={"placeholder": "Skrocona nazwa"}),
            "code": forms.TextInput(attrs={"placeholder": "Kod laboratorium"}),
            "address": forms.TextInput(attrs={"placeholder": "Adres"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["technicians"].queryset = User.objects.filter(role="technician").order_by("username")
        self.fields["managers"].queryset = User.objects.filter(role="manager").order_by("username")
        self.fields["technicians"].required = False
        self.fields["managers"].required = False
        self.fields["technicians"].help_text = "Wybierz technikow pracujacych w laboratorium."
        self.fields["managers"].help_text = "Wybierz kierownikow odpowiedzialnych za laboratorium."
