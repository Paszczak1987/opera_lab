from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import WorksiteForm
from .models import Worksite


class WorksiteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Worksite
    form_class = WorksiteForm
    template_name = "worksites/worksite_form.html"
    success_url = reverse_lazy("home:logged_in")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.role == "client":
            self.object.clients.add(self.request.user)
        messages.success(self.request, "Budowa została pomyślnie dodana.")
        return response

    def test_func(self):
        return self.request.user.role in {"admin", "client"}

    def get_success_url(self):
        scope = "mine" if self.request.user.role == "client" else "all"
        base = reverse_lazy("worksites:list")
        return f"{base}?section=worksites&scope={scope}"


class WorksiteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Worksite
    template_name = "worksites/worksite_list.html"
    context_object_name = "worksites"
    paginate_by = 20

    def test_func(self):
        return self.request.user.role in {"admin", "client"}

    def get_scope(self):
        scope = self.request.GET.get("scope") or ""
        if scope not in {"all", "mine"}:
            scope = "mine" if self.request.user.role == "client" else "all"
        return scope

    def get_queryset(self):
        qs = Worksite.objects.prefetch_related("clients").order_by("name")
        scope = self.get_scope()
        user = self.request.user
        if scope == "mine":
            return qs.filter(clients=user).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scope"] = self.get_scope()
        context["section"] = "worksites"
        return context
