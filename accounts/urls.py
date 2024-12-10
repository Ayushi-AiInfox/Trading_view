
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
   
]





