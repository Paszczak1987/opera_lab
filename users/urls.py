from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('client/', views.ClientDashboardView.as_view(), name='client_dashboard'),
    path('manager/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('technician/', views.TechnicianDashboardView.as_view(), name='technician_dashboard'),
    path('viewer/', views.ViewerDashboardView.as_view(), name='viewer_dashboard'),
    path('profile/', views.ProfileSettingsView.as_view(), name='profile_settings'),
]
