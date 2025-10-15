from django import forms
from django.contrib.auth import get_user_model

from .models import Worksite


# FIELD_CLASS = "w-full px-3 py-2 bg-neutral-900 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500"


class WorksiteForm(forms.ModelForm):
    class Meta:
        model = Worksite
        fields = ["name", "short_name", "code", "office_address", "clients"]
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
