
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:  
                login(request, user)
                return redirect('admin_dashboard')  
            else:
                messages.error(request, "You are not authorized to access the admin dashboard.")
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'accounts/login.html')
