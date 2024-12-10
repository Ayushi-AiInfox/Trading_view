from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# View for the root path to redirect to the login page
def root_redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('accounts/login')    # If logged in, go to the home page (dashboard)
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),  # Redirect root to login if not logged in
    path('accounts/', include('accounts.urls')),  # Include accounts app URLs (login, signup, etc.)
]





from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
