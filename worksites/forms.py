from django import forms
from django.contrib.auth import get_user_model

from .models import Worksite


# FIELD_CLASS = "w-full px-3 py-2 bg-neutral-900 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"


class WorksiteForm(forms.ModelForm):
    class Meta:
        model = Worksite
        fields = ["name", "short_name", "code", "office_address", "clients"]
        labels = {
            'name': "Pełna nazwa budowy",
            'short_name': "Skrócona nazwa",
            'code': "Kod budowy",
            'office_address': "Adres biura budowy",
            'clients': "Zamawiający",
        }
        widgets = {
            # "name": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Pełna nazwa budowy"}),
            # "short_name": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Skrócona nazwa"}),
            # "code": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Kod budowy"}),
            # "office_address": forms.TextInput(attrs={"class": FIELD_CLASS, "placeholder": "Adres biura budowy"}),
            # "clients": forms.SelectMultiple(attrs={"class": FIELD_CLASS}),
            "name": forms.TextInput(attrs={"placeholder": "Pełna nazwa budowy"}),
            "short_name": forms.TextInput(attrs={"placeholder": "Skrócona nazwa"}),
            "code": forms.TextInput(attrs={"placeholder": "Kod budowy"}),
            "office_address": forms.TextInput(attrs={"placeholder": "Adres biura budowy"}),
            "clients": forms.SelectMultiple(attrs={}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        user_model = get_user_model()
        self.fields["clients"].queryset = user_model.objects.filter(role="client").order_by("username")
        self.fields["clients"].help_text = "Wybierz klientów powiązanych z budową."
        if user and user.role == "client":
            self.fields["clients"].initial = [user]
            self.fields["clients"].widget = forms.MultipleHiddenInput()
            self.fields["clients"].help_text = "Zostaniesz przypisany jako zamawiajcy tej budowy."
        self.fields["clients"].required = False
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
