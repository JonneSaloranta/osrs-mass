from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_event, name='create'),
    path('join/', views.join, name='join'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('leave/<int:id>/', views.leave, name='leave'),
    path('details/<uuid:uuid>/', views.details, name='details'),
]
