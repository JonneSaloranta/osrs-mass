from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate_email'),
    path('request-activation/', views.request_activation_email, name='request_activation_email'),
]