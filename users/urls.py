from django.urls import path
from .views import LoginView, ProfileView, SignUpView,  logout_view, UserUpdateView

urlpatterns = [
    path('login', LoginView.as_view(), name='sign-in'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('signup', SignUpView.as_view(), name='sign-up'),
    path('logout', logout_view, name='logout'),
    path('update/profile', UserUpdateView.as_view(), name='update-profile')

]