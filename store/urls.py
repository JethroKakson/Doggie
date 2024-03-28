from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'), # we name them login_user because django also has a function called login.
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]