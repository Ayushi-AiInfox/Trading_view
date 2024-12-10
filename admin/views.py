from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import jwt
from django.contrib import messages
from django.conf import settings
from accounts.models import User  
KEYS = getattr(settings, "KEY", None)


def AdminDashboardView(request):
    if request.session.has_key('token'):
        token = request.session.get('token')
        try:
            d = jwt.decode(token, key=KEYS, algorithms=['HS256'])
            usr = User.objects.get(email = d.get("email"))
            if d.get('method')!="verified" or usr.role!='admin':
                return redirect('../../accounts/login')
        except:
            return redirect('../../accounts/login')
        if 'message' in request.session:
            messages.success(request, "Login successful!")
            del request.session['message'] 
    
        return render(request,'admin_dashboard.html')
    else:
        return redirect('../../accounts/login')
    

