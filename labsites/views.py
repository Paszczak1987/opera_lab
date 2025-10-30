from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import LabSiteForm
from .models import LabSite


class AdminOnlyMixin(UserPassesTestMixin):
    """Ensure only admins can access the view."""

    def test_func(self):
        user = self.request.user
        return getattr(user, "role", None) == "admin"


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
                "assigned_managers": laboratory.managers.order_by("username").all(),
                "assigned_technicians": laboratory.technicians.order_by("username").all(),
                "assigned_personnel": laboratory.managers.count() + laboratory.technicians.count(),
            }
        )
        return context
