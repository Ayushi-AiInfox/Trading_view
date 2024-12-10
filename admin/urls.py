

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]


