from django.urls import path

from .views import LabSiteCreateView, LabSiteDetailView, LabSiteListView, ManagerActiveLabSiteView

app_name = "labsites"

urlpatterns = [
    path("", LabSiteListView.as_view(), name="list"),
    path("create/", LabSiteCreateView.as_view(), name="create"),
    path("manager/active/", ManagerActiveLabSiteView.as_view(), name="manager_active"),
    path("<int:pk>/", LabSiteDetailView.as_view(), name="detail"),
]
