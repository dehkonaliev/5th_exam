from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


class ProfileView(View):
    def get(self, request):
        return render(request, 'users/profile.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')