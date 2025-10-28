from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Ensure only users with the matching role can access the view."""

    required_role: str | None = None

    def test_func(self):
        user = self.request.user
        return bool(getattr(user, "role", None) == self.required_role)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class RoleDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "users/dashboard.html"
    dashboard_title = "Panel uzytkownika"
    dashboard_message = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "dashboard_title": self.dashboard_title,
                "dashboard_message": self.dashboard_message,
            }
        )
        return context


class AdminDashboardView(RoleDashboardView):
    required_role = "admin"
    dashboard_title = "Panel administratora"
    dashboard_message = (
        "Zarzadzaj konfiguracja systemu oraz kontami innych uzytkownikow."
    )


class ClientDashboardView(RoleDashboardView):
    required_role = "client"
    dashboard_title = "Panel klienta"
    dashboard_message = (
        "Twórz i wysyłaj zlecenia. Sprawdzaj postep zlecen, otrzymuj raporty oraz komunikaty dotyczace realizacji."
    )


class ManagerDashboardView(RoleDashboardView):
    required_role = "manager"
    dashboard_title = "Panel kierownika"
    dashboard_message = (
        "Planowanie pracy zespolu, kontrola nad zleceniami. Tworzenie, wykonywanie, edycja badań i sprawozdań"
    )


class TechnicianDashboardView(RoleDashboardView):
    required_role = "technician"
    dashboard_title = "Panel technika"
    dashboard_message = (
        "Lista probek oraz instrukcje badawcze pojawia sie w tym miejscu."
    )


class ViewerDashboardView(RoleDashboardView):
    required_role = "viewer"
    dashboard_title = "Panel obserwatora"
    dashboard_message = "Przegladaj raporty i statystyki bez mozliwosci edycji."


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_settings.html"
