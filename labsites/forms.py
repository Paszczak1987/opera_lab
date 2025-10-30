from django import forms

from users.models import User

from .models import LabSite


class AssignmentAwareSelectMultiple(forms.SelectMultiple):
    """Select widget that adds classes for users assigned to any laboratory."""

    option_inherits_attrs = False

    def __init__(
        self,
        *args,
        assigned_ids=None,
        assigned_class="",
        available_class="",
        **kwargs,
    ):
        self.assigned_ids = {str(value) for value in (assigned_ids or [])}
        self.assigned_class = assigned_class
        self.available_class = available_class
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value is not None:
            option_attrs = option.setdefault("attrs", {})
            classes = option_attrs.get("class", "").split()
            if str(value) in self.assigned_ids and self.assigned_class:
                classes.append(self.assigned_class)
                option_attrs["data-assigned"] = "true"
                # Inline style ensures consistent desaturated color across browsers.
                existing_style = option_attrs.get("style", "")
                option_attrs["style"] = f"{existing_style}color:#64748b;".strip()
            elif self.available_class:
                classes.append(self.available_class)
                option_attrs["data-assigned"] = "false"
                existing_style = option_attrs.get("style", "")
                option_attrs["style"] = f"{existing_style}color:#e2e8f0;".strip()
            if classes:
                option_attrs["class"] = " ".join(classes)
        return option


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
        labels = {
            'name': "Nazwa laboratorium",
            'short_name': "Skrocona nazwa",
            'code': "Kod laboratorium",
            'address': "Adres",
            'technicians': "Technicy",
            'managers': "Kierownicy",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Pelna nazwa laboratorium"}),
            "short_name": forms.TextInput(attrs={"placeholder": "Skrocona nazwa"}),
            "code": forms.TextInput(attrs={"placeholder": "Kod laboratorium"}),
            "address": forms.TextInput(attrs={"placeholder": "Adres"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        technicians_qs = User.objects.filter(role="technician").order_by("username")
        managers_qs = User.objects.filter(role="manager").order_by("username")
        self.fields["technicians"].queryset = technicians_qs
        self.fields["managers"].queryset = managers_qs
        self.fields["technicians"].required = False
        self.fields["managers"].required = False
        self.fields["technicians"].help_text = "Wybierz technikow pracujacych w laboratorium."
        self.fields["managers"].help_text = "Wybierz kierownikow odpowiedzialnych za laboratorium."

        technician_assigned_ids = technicians_qs.filter(laboratories__isnull=False).values_list("id", flat=True)
        manager_assigned_ids = managers_qs.filter(managed_laboratories__isnull=False).values_list("id", flat=True)

        base_select_classes = (
            "w-full bg-slate-900/70 border border-slate-600 rounded px-3 py-2 "
            "text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500 "
            "focus:border-transparent min-h-[12rem] custom-scrollbar"
        )

        self.fields["technicians"].widget = AssignmentAwareSelectMultiple(
            attrs={"class": base_select_classes, "data-field": "technicians"},
            assigned_ids=technician_assigned_ids,
            assigned_class="option-assigned",
            available_class="option-available",
            choices=self.fields["technicians"].choices,
        )
        self.fields["managers"].widget = AssignmentAwareSelectMultiple(
            attrs={"class": base_select_classes, "data-field": "managers"},
            assigned_ids=manager_assigned_ids,
            assigned_class="option-assigned",
            available_class="option-available",
            choices=self.fields["managers"].choices,
        )
