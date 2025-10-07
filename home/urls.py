from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeMainView.as_view(), name='home'),
]