from django import forms

from config.countries import DEFAULT_COUNTRY_CODE, country_choices
from users.models import User

from .models import LabSite
from .widgets import ManagerDualListWidget, TechnicianDualListWidget


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
            elif self.available_class:
                classes.append(self.available_class)
                option_attrs["data-assigned"] = "false"
            if classes:
                option_attrs["class"] = " ".join(classes)
        return option


class LabSiteAdminForm(forms.ModelForm):
    """Custom form for managing laboratories in admin."""

    class Meta:
        model = LabSite
        fields = ["name", "short_name", "code", "address", "country_code", "technicians", "managers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["technicians"].queryset = User.objects.filter(role="technician")
        self.fields["managers"].queryset = User.objects.filter(role="manager")
        self.fields["country_code"].widget = forms.Select(choices=country_choices())
        self.fields["country_code"].label = "Kraj"
        self.fields["country_code"].help_text = "Wybierz kraj, w ktorym dziala laboratorium."
        for field in ("technicians", "managers"):
            self.fields[field].help_text = ""


class LabSiteForm(forms.ModelForm):
    """Form used in the dashboard for creating or editing laboratories."""

    class Meta:
        model = LabSite
        fields = ["name", "short_name", "code", "country_code", "address", "technicians", "managers"]
        labels = {
            'name': "Nazwa laboratorium",
            'short_name': "Skrocona nazwa",
            'code': "Kod laboratorium",
            'country_code': "Kraj",
            'address': "Adres",
            'technicians': "Technicy",
            'managers': "Kierownicy",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Pelna nazwa laboratorium"}),
            "short_name": forms.TextInput(attrs={"placeholder": "Skrocona nazwa"}),
            "code": forms.TextInput(attrs={"placeholder": "Kod laboratorium"}),
            "country_code": forms.Select(attrs={}),
            "address": forms.TextInput(attrs={"placeholder": "Adres"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        technicians_qs = (
            User.objects.filter(role="technician")
            .prefetch_related("laboratories")
            .order_by("username")
        )
        managers_qs = (
            User.objects.filter(role="manager")
            .prefetch_related("managed_laboratories")
            .order_by("username")
        )
        self.fields["technicians"].queryset = technicians_qs
        self.fields["managers"].queryset = managers_qs
        self.fields["country_code"].choices = country_choices()
        self.fields["country_code"].initial = self.instance.country_code or DEFAULT_COUNTRY_CODE
        self.fields["technicians"].required = False
        self.fields["managers"].required = False
        for field_name in ("technicians", "managers"):
            self.fields[field_name].help_text = ""

        selected_technician_ids = self._determine_selected_technician_ids()
        self._build_technician_option_lists(technicians_qs, selected_technician_ids)
        self.fields["technicians"].widget = TechnicianDualListWidget(
            available_options=self.available_technicians,
            selected_options=self.selected_technicians,
        )

        self._build_manager_option_lists(managers_qs, self._determine_selected_manager_ids())
        self.fields["managers"].widget = ManagerDualListWidget(
            available_options=self.available_managers,
            selected_options=self.selected_managers,
        )
        self.fields["country_code"].widget.attrs.update(
            {
                "class": (
                    "w-full bg-slate-900/70 border border-slate-600 px-3 py-2 "
                    "text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500 "
                    "focus:border-transparent"
                )
            }
        )

    def _determine_selected_technician_ids(self) -> set[str]:
        """Return technician IDs that should start in the assigned list."""
        if self.is_bound:
            data_list = self.data.getlist(self.add_prefix("technicians"))
            return {str(value) for value in data_list}
        if self.initial.get("technicians"):
            return {str(value) for value in self.initial["technicians"]}
        if self.instance.pk:
            return {
                str(value)
                for value in self.instance.technicians.values_list("id", flat=True)
            }
        return set()

    def _build_technician_option_lists(self, technicians_qs, selected_ids: set[str]) -> None:
        """Prepare collections used to render the dual-list widget."""
        current_lab_id = self.instance.pk if self.instance and self.instance.pk else None
        available_options: list[dict[str, str | bool]] = []
        selected_options: list[dict[str, str | bool]] = []

        for technician in technicians_qs:
            full_name = (technician.get_full_name() or "").strip()
            display_name = full_name or technician.username
            laboratories = list(technician.laboratories.all())
            lab_short_names = [lab.short_name for lab in laboratories]
            if current_lab_id is not None:
                other_lab_short_names = [lab.short_name for lab in laboratories if lab.pk != current_lab_id]
            else:
                other_lab_short_names = lab_short_names[:]
            assigned_anywhere = bool(lab_short_names)
            locked_for_assignment = bool(other_lab_short_names)

            if assigned_anywhere:
                lab_listing = ", ".join(sorted(lab_short_names))
                display_label = f"{display_name} ({lab_listing})"
            else:
                display_label = display_name

            option = {
                "id": str(technician.pk),
                "label": display_label,
                "assigned_elsewhere": assigned_anywhere,
                "locked": locked_for_assignment and str(technician.pk) not in selected_ids,
                "original_locked": locked_for_assignment,
                "css_class": "option-assigned" if assigned_anywhere else "option-available",
            }

            if option["id"] in selected_ids:
                option["locked"] = False
                option["css_class"] = "option-available"
                selected_options.append(option)
            else:
                available_options.append(option)

        available_options.sort(key=lambda opt: str(opt["label"]).lower())
        selected_options.sort(key=lambda opt: str(opt["label"]).lower())

        self.available_technicians = available_options
        self.selected_technicians = selected_options
        self.fields["technicians"].choices = [
            (opt["id"], opt["label"]) for opt in available_options + selected_options
        ]

    def _determine_selected_manager_ids(self) -> set[str]:
        if self.is_bound:
            return {str(value) for value in self.data.getlist(self.add_prefix("managers"))}
        if self.initial.get("managers"):
            return {str(value) for value in self.initial["managers"]}
        if self.instance.pk:
            return {str(value) for value in self.instance.managers.values_list("id", flat=True)}
        return set()

    def _build_manager_option_lists(self, managers_qs, selected_ids: set[str]) -> None:
        available_options: list[dict[str, str | bool]] = []
        selected_options: list[dict[str, str | bool]] = []

        for manager in managers_qs:
            full_name = (manager.get_full_name() or "").strip()
            display_name = full_name or manager.username
            laboratories = list(manager.managed_laboratories.all())
            lab_short_names = [lab.short_name for lab in laboratories]
            assigned_anywhere = bool(lab_short_names)
            if assigned_anywhere:
                lab_listing = ", ".join(sorted(lab_short_names))
                display_label = f"{display_name} ({lab_listing})"
            else:
                display_label = display_name

            option = {
                "id": str(manager.pk),
                "label": display_label,
                "assigned_elsewhere": assigned_anywhere,
                "locked": False,
                "original_locked": False,
                "css_class": "option-assigned" if assigned_anywhere else "option-available",
            }

            if option["id"] in selected_ids:
                selected_options.append(option)
            else:
                available_options.append(option)

        available_options.sort(key=lambda opt: str(opt["label"]).lower())
        selected_options.sort(key=lambda opt: str(opt["label"]).lower())

        self.available_managers = available_options
        self.selected_managers = selected_options
        self.fields["managers"].choices = [
            (opt["id"], opt["label"]) for opt in available_options + selected_options
        ]


class ManagerActiveLabSelectionForm(forms.Form):
    """Dropdown for managers to switch the active laboratory."""

    laboratory = forms.ModelChoiceField(
        label="Aktywne laboratorium",
        queryset=LabSite.objects.none(),
        required=True,
        empty_label=None,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        managed_qs = LabSite.objects.filter(managers=user).order_by("name") if user else LabSite.objects.none()
        self.fields["laboratory"].queryset = managed_qs
        if user and getattr(user, "active_laboratory_id", None):
            self.fields["laboratory"].initial = user.active_laboratory_id
        self.fields["laboratory"].widget.attrs.update(
            {
                "class": (
                    "w-full bg-slate-900/70 border border-slate-600 px-3 py-2 text-sm text-gray-200 "
                    "focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                )
            }
        )
