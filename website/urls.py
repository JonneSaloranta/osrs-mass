
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.change_nickname, name='change_nickname'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
]