from django import forms
from django.contrib.auth import get_user_model

from config.countries import DEFAULT_COUNTRY_CODE, country_choices
from .models import Worksite


class WorksiteForm(forms.ModelForm):
    class Meta:
        model = Worksite
        fields = ["name", "short_name", "code", "country_code", "office_address", "clients"]
        labels = {
            "name": "Pelna nazwa budowy",
            "short_name": "Skrocona nazwa",
            "code": "Kod budowy",
            "country_code": "Kraj",
            "office_address": "Adres biura budowy",
            "clients": "Zamawiajacy",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Pelna nazwa budowy"}),
            "short_name": forms.TextInput(attrs={"placeholder": "Skrocona nazwa"}),
            "code": forms.TextInput(attrs={"placeholder": "Kod budowy"}),
            "country_code": forms.Select(),
            "office_address": forms.TextInput(attrs={"placeholder": "Adres biura budowy"}),
            "clients": forms.SelectMultiple(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        user_model = get_user_model()

        self.fields["country_code"].choices = country_choices()
        self.fields["country_code"].initial = self.instance.country_code or DEFAULT_COUNTRY_CODE
        self.fields["country_code"].widget.attrs.update(
            {
                "class": (
                    "w-full bg-slate-900/70 border border-slate-600 rounded px-3 py-2 "
                    "text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500 "
                    "focus:border-transparent"
                )
            }
        )

        self.fields["clients"].queryset = user_model.objects.filter(role="client").order_by("username")
        self.fields["clients"].required = False
        self.fields["clients"].help_text = "Wybierz klientow powiazanych z budowa."

        if user and user.role == "client":
            self.fields["clients"].initial = [user]
            self.fields["clients"].widget = forms.MultipleHiddenInput()
            self.fields["clients"].help_text = "Zostaniesz przypisany jako zamawiajacy tej budowy."

        if not isinstance(self.fields["clients"].widget, forms.MultipleHiddenInput):
            base_select_classes = (
                "w-full bg-slate-900/70 border border-slate-600 rounded px-3 py-2 "
                "text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500 "
                "focus:border-transparent min-h-[10rem] custom-scrollbar"
            )
            self.fields["clients"].widget.attrs.update(
                {
                    "class": base_select_classes,
                    "data-field": "clients",
                }
            )
