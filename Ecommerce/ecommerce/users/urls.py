from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = "login"),
    path('register/', views.registeration, name = "register"),
    path('logout/', auth_views.LogoutView.as_view(template_name='posts/homepage.html'), name = "logout"),
    path('profile/',views.user_profile,name = "profile"),
]
