from django.urls import path

from .views import WorksiteCreateView, WorksiteListView

app_name = "worksites"

urlpatterns = [
    path("", WorksiteListView.as_view(), name="list"),
    path("create/", WorksiteCreateView.as_view(), name="create"),
]
