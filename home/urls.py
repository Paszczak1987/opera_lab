from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeMainView.as_view(), name='home'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('logout/', views.logout_view, name='logout'),
]