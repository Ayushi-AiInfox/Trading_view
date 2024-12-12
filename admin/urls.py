from django.urls import path
from . import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
  
    path('dashboard/', views.AdminDashboardView, name='admin_dashboard'),
    path('save-symbol/', views.SaveSymbol,name= 'saving_symbol'),
    path('save-interval/',views.saveInterval,name='save interval')

]

