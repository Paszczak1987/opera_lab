from __future__ import annotations

from django import forms


class DualListWidget(forms.Widget):
    """Reusable dual-list widget with transfer buttons."""

    template_name = "labsites/widgets/dual_list.html"
    base_select_classes = (
        "w-full bg-slate-900/70 border border-slate-600 rounded-none px-3 py-2 "
        "text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-teal-500 "
        "focus:border-transparent min-h-[12rem] custom-scrollbar"
    )

    def __init__(
        self,
        attrs: dict | None = None,
        *,
        prefix: str,
        available_label: str,
        selected_label: str,
        add_label: str = "Dodaj >>",
        remove_label: str = "<< Usun",
        available_options: list[dict] | None = None,
        selected_options: list[dict] | None = None,
    ) -> None:
        attrs = attrs.copy() if attrs else {}
        extra_classes = attrs.pop("class", "")
        if extra_classes:
            select_classes = f"{extra_classes} {self.base_select_classes}"
        else:
            select_classes = self.base_select_classes

        default_attrs = {
            "id": f"{prefix}-selected",
            "data-role": "selected",
            "data-dual-key": prefix,
            "class": select_classes,
            "multiple": "multiple",
        }
        default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.prefix = prefix
        self.available_label = available_label
        self.selected_label = selected_label
        self.add_label = add_label
        self.remove_label = remove_label
        self.available_options = available_options or []
        self.selected_options = selected_options or []
        self.select_classes = select_classes

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["available_options"] = self.available_options
        context["selected_options"] = self.selected_options
        context["available_attrs"] = {
            "id": f"{self.prefix}-available",
            "data-role": "available",
            "data-dual-key": self.prefix,
            "class": self.select_classes,
            "multiple": "multiple",
        }
        context["titles"] = {
            "available": self.available_label,
            "selected": self.selected_label,
        }
        context["buttons"] = {
            "add": {"id": f"{self.prefix}-add", "label": self.add_label},
            "remove": {"id": f"{self.prefix}-remove", "label": self.remove_label},
        }
        context["wrapper_attrs"] = {"data-dual-list": self.prefix}
        return context

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)


class TechnicianDualListWidget(DualListWidget):
    """Dual-list widget configured for technicians."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            prefix="technicians",
            available_label="Wybierz ostepnych techników",
            selected_label="Technicy przypisani do nowego laboratorium",
            **kwargs,
        )


class ManagerDualListWidget(DualListWidget):
    """Dual-list widget configured for managers."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            prefix="managers",
            available_label="Dostepni kierownicy",
            selected_label="Kierownicy w laboratorium",
            **kwargs,
        )
