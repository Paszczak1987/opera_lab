from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeMainView.as_view(), name='home'),
    path('logged_in/', views.WelcomeView.as_view(), name='logged_in'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]