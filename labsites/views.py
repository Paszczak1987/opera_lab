from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView

from .forms import LabSiteForm, ManagerActiveLabSelectionForm
from .models import LabSite


def build_labsite_assignments_context(laboratory: LabSite | None) -> dict:
    """Prepare personnel lists for laboratory detail views."""
    if laboratory is None:
        return {
            "assigned_managers": [],
            "assigned_technicians": [],
            "assigned_personnel": 0,
        }

    managers = list(laboratory.managers.order_by("username").all())
    technicians = list(laboratory.technicians.order_by("username").all())
    return {
        "assigned_managers": managers,
        "assigned_technicians": technicians,
        "assigned_personnel": len(managers) + len(technicians),
    }


class AdminOnlyMixin(UserPassesTestMixin):
    """Ensure only admins can access the view."""

    def test_func(self):
        user = self.request.user
        return getattr(user, "role", None) == "admin"


class ManagerOnlyMixin(UserPassesTestMixin):
    """Ensure only managers can access the view."""

    def test_func(self):
        user = self.request.user
        return getattr(user, "role", None) == "manager"


class LabSiteListView(LoginRequiredMixin, AdminOnlyMixin, ListView):
    model = LabSite
    template_name = "labsites/labsite_list.html"
    context_object_name = "laboratories"
    paginate_by = 20

    def get_queryset(self):
        return LabSite.objects.prefetch_related("technicians", "managers").order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "section": "laboratories",
                "dashboard_title": "Laboratoria",
                "dashboard_message": "Zarzadzaj lista laboratoriow i przypisanym personelem.",
            }
        )
        return context


class LabSiteCreateView(LoginRequiredMixin, AdminOnlyMixin, CreateView):
    model = LabSite
    form_class = LabSiteForm
    template_name = "labsites/labsite_form.html"
    success_url = reverse_lazy("labsites:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Laboratorium zostalo pomyslnie utworzone.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "section": "laboratories",
                "dashboard_title": "Nowe laboratorium",
                "dashboard_message": "Stworz rekord laboratorium i przypisz personel.",
            }
        )
        return context

    def get_success_url(self):
        base = super().get_success_url()
        return f"{base}?section=laboratories"


class LabSiteDetailView(LoginRequiredMixin, AdminOnlyMixin, DetailView):
    model = LabSite
    template_name = "labsites/labsite_detail.html"
    context_object_name = "laboratory"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laboratory: LabSite = context["laboratory"]
        context.update(
            {
                "section": "laboratories",
                "dashboard_title": laboratory.name,
                "dashboard_message": "Szczegoly laboratorium oraz przypisany personel.",
            }
        )
        context.update(build_labsite_assignments_context(laboratory))
        return context


class ManagerActiveLabSiteView(LoginRequiredMixin, ManagerOnlyMixin, FormView):
    template_name = "labsites/labsite_detail.html"
    form_class = ManagerActiveLabSelectionForm

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get" and request.GET.get("section") != "laboratory":
            query = request.GET.copy()
            query["section"] = "laboratory"
            return HttpResponseRedirect(f"{request.path}?{query.urlencode()}")

        self.managed_laboratories = list(
            LabSite.objects.filter(managers=request.user)
            .prefetch_related("technicians", "managers")
            .order_by("name")
        )
        self._active_laboratory_cache = None
        self._active_laboratory_cache_ready = False
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def ensure_active_laboratory(self):
        if getattr(self, "_active_laboratory_cache_ready", False):
            return self._active_laboratory_cache

        user = self.request.user
        active = user.active_laboratory
        managed_by_id = {lab.pk: lab for lab in self.managed_laboratories}
        matched = None

        if active and active.pk in managed_by_id:
            matched = managed_by_id[active.pk]
        elif active:
            user.active_laboratory = None
            user.save(update_fields=["active_laboratory"])
            active = None

        if matched is None and self.managed_laboratories:
            first_lab = self.managed_laboratories[0]
            if active is None or active.pk != first_lab.pk:
                user.active_laboratory = first_lab
                user.save(update_fields=["active_laboratory"])
            matched = first_lab

        self._active_laboratory_cache = matched
        self._active_laboratory_cache_ready = True
        return matched

    def get_initial(self):
        initial = super().get_initial()
        active_lab = self.ensure_active_laboratory()
        if active_lab:
            initial["laboratory"] = active_lab.pk
        return initial

    def form_valid(self, form):
        laboratory = form.cleaned_data["laboratory"]
        user = self.request.user
        if laboratory and user.active_laboratory_id != laboratory.id:
            user.active_laboratory = laboratory
            user.save(update_fields=["active_laboratory"])
            self._active_laboratory_cache = laboratory
            self._active_laboratory_cache_ready = True
            messages.success(self.request, "Aktywne laboratorium zostalo zmienione.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        query = self.request.GET.copy()
        query["section"] = "laboratory"
        query_string = query.urlencode()
        return f"{self.request.path}?{query_string}" if query_string else f"{self.request.path}?section=laboratory"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_lab = self.ensure_active_laboratory()
        context["laboratory"] = active_lab
        context["section"] = "laboratory"
        context["dashboard_title"] = active_lab.name if active_lab else "Laboratorium"
        context["dashboard_message"] = (
            "Szczegoly laboratorium oraz przypisany personel."
            if active_lab
            else "Nie masz przypisanego aktywnego laboratorium."
        )
        context.update(build_labsite_assignments_context(active_lab))
        if len(self.managed_laboratories) > 1:
            context["laboratory_switch_form"] = context.get("form")
        context["has_managed_laboratories"] = bool(self.managed_laboratories)
        return context
